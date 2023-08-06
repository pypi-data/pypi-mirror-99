import filecmp
import json
import os
import re
import shutil
import six

from typing import Union, Optional

from DKCloudCommand.modules.DKIgnore import DKIgnore

from DKCloudCommand.modules.githash import githash_by_file_name

from DKCloudCommand.modules.DKKitchenDisk import DKKitchenDisk
from DKCloudCommand.modules.DKFileHelper import DKFileHelper

__author__ = "DataKitchen, Inc."

from DKCommon.DKTypeUtils import JSONData

RECIPE_META = "RECIPE_META"
DK_CONFLICTS_META = "conflicts.json"
ORIG_HEAD = "ORIG_HEAD"
FILE_SHA = "FILE_SHA"


class DKRecipeDisk:
    def __init__(
        self,
        ignore: DKIgnore,
        recipe_sha: Optional[str] = None,
        recipe: Optional[JSONData] = None,
        path: Optional[str] = None,
    ) -> None:
        self.ignore = ignore
        self.recipe = recipe
        self._recipe_sha = recipe_sha
        self._recipe_path = path
        if recipe:
            self._recipe_name = min(recipe.keys()) if len(list(recipe.keys())) else ""

            if os.sep in self._recipe_name:
                self._recipe_name = self._recipe_name.split(os.sep)[0]

            self._kitchen_meta_dir = DKKitchenDisk.find_kitchen_meta_dir(path)
            self._recipes_meta_dir = DKKitchenDisk.get_recipes_meta_dir(self._kitchen_meta_dir)
            self._recipe_meta_dir = os.path.join(self._recipes_meta_dir, self._recipe_name)

    # For  each recipe_file_key (key), file_list (value) in the dictionary
    #   if the directory exists
    #     delete it
    #   create the directory
    #   for each file in the file_list
    #     create the file
    #     write the contents
    #   write our metadata to the kitchen folder (.dk)
    def save_recipe_to_disk(self, update_meta: bool = True) -> Optional[bool]:
        recipe_dict = self.recipe
        root_dir = self._recipe_path

        if isinstance(recipe_dict, dict) is False:
            return None
        if root_dir is None:
            return None

        if update_meta:
            if not self.write_recipe_meta(root_dir):
                return None

        for recipe_file_key, files_list in six.iteritems(recipe_dict):
            if len(recipe_file_key) > 0:
                full_dir = os.path.join(root_dir, recipe_file_key)
            else:
                return None
                # full_dir = root_dir  # original code, when does this happen?
            if os.path.isdir(full_dir) is False:
                try:
                    os.makedirs(full_dir)
                except Exception:
                    return None
            if isinstance(files_list, list) is False:
                return None
            for file_dict in files_list:
                if isinstance(file_dict, dict) is False:
                    return None
                self.write_files(full_dir, file_dict)

        self.write_recipe_state_from_kitchen(root_dir)
        self.write_orig_head()

        return True

    def write_recipe_meta(self, start_dir: str) -> bool:
        if not DKKitchenDisk.is_kitchen_root_dir(start_dir):
            print(f"'{start_dir}' is not a Kitchen directory")
            return False

        kitchen_meta_dir = DKKitchenDisk.find_kitchen_meta_dir(start_dir)
        if kitchen_meta_dir is None:
            print(f"Unable to find kitchen meta directory in '{start_dir}'")
            return False
        recipes_meta_dir = DKKitchenDisk.get_recipes_meta_dir(kitchen_meta_dir)
        if recipes_meta_dir is None:
            print(f"Unable to find recipes meta directory in '{start_dir}'")
            return False

        recipe_meta_dir = os.path.join(recipes_meta_dir, self._recipe_name)
        if not os.path.isdir(recipe_meta_dir):
            try:
                os.makedirs(recipe_meta_dir)
            except OSError as e:
                print(f"{e.filename} - {e.errno} - {e}")
                return False
        recipes_meta_file = os.path.join(recipe_meta_dir, RECIPE_META)
        try:
            DKFileHelper.write_file(recipes_meta_file, self._recipe_name)
        except OSError as e:
            print(f"{e.filename} - {e.errno} - {e}")
            return False

        return self.write_orig_head()

    def write_orig_head(self) -> bool:
        orig_head_file = os.path.join(self._recipe_meta_dir, ORIG_HEAD)
        try:
            DKFileHelper.write_file(orig_head_file, self._recipe_sha)
        except OSError as e:
            print(f"{e.filename} - {e.errno} - {e}")
            return False
        return True

    def write_recipe_state_from_kitchen(self, start_dir: str) -> Optional[bool]:
        if not DKKitchenDisk.is_kitchen_root_dir(start_dir):
            print(f"'{start_dir}' is not a Kitchen directory")
            return False
        self.write_recipe_state(os.path.join(start_dir, self._recipe_name), self.recipe)

    def write_recipe_state(self, recipe_dir: str, remote_shas: Optional[JSONData] = None) -> Optional[bool]:

        kitchen_meta_dir = DKKitchenDisk.find_kitchen_meta_dir(recipe_dir)
        if kitchen_meta_dir is None:
            print(f"Unable to find kitchen meta directory in '{recipe_dir}'")
            return False
        recipes_meta_dir = DKKitchenDisk.get_recipes_meta_dir(kitchen_meta_dir)
        if recipes_meta_dir is None:
            print(f"Unable to find recipes meta directory in '{recipe_dir}'")
            return False

        _, recipe_name = os.path.split(recipe_dir)

        recipe_meta_dir = os.path.join(recipes_meta_dir, recipe_name)

        recipe_sha_file = os.path.join(recipe_meta_dir, FILE_SHA)

        shas = dict()
        if os.path.isfile(recipe_sha_file):
            if remote_shas:
                shas = DKRecipeDisk.load_saved_shas(recipe_meta_dir)
                for remote_recipe_name, remote_files in six.iteritems(remote_shas):
                    for remote_file in remote_files:
                        file_name = str(os.path.join(remote_recipe_name, remote_file["filename"]))
                        shas[file_name] = str(remote_file["sha"])
            else:
                pass  # do nothing if remote shas are not provided
        else:  # a new recipe
            shas = self.fetch_shas(recipe_dir)

        if len(shas) > 0:
            DKFileHelper.write_file(recipe_sha_file, "\n".join([f"{k}:{v}" for k, v in shas.items()]))

    @staticmethod
    def write_recipe_state_file_add(recipe_dir: str, file_recipe_path: str) -> Optional[bool]:
        kitchen_meta_dir = DKKitchenDisk.find_kitchen_meta_dir(recipe_dir)
        if kitchen_meta_dir is None:
            print(f"Unable to find kitchen meta directory in '{recipe_dir}'")
            return False
        recipes_meta_dir = DKKitchenDisk.get_recipes_meta_dir(kitchen_meta_dir)
        if recipes_meta_dir is None:
            print(f"Unable to find recipes meta directory in '{recipe_dir}'")
            return False

        _, recipe_name = os.path.split(recipe_dir)
        recipe_meta_dir = os.path.join(recipes_meta_dir, recipe_name)
        recipe_sha_file = os.path.join(recipe_meta_dir, FILE_SHA)

        contents = DKFileHelper.read_file(recipe_sha_file)
        the_path = os.path.join(recipe_name, file_recipe_path)
        full_file_path = os.path.join(recipe_dir, file_recipe_path)
        the_sha = githash_by_file_name(full_file_path)
        new_line = f"\n{the_path}:{the_sha}"
        contents += new_line
        new_contents = contents.strip("\n")
        DKFileHelper.write_file(recipe_sha_file, new_contents)

    @staticmethod
    def write_recipe_state_file_delete(recipe_dir: str, file_recipe_path: str) -> Optional[bool]:
        kitchen_meta_dir = DKKitchenDisk.find_kitchen_meta_dir(recipe_dir)
        if kitchen_meta_dir is None:
            print(f"Unable to find kitchen meta directory in '{recipe_dir}'")
            return False
        recipes_meta_dir = DKKitchenDisk.get_recipes_meta_dir(kitchen_meta_dir)
        if recipes_meta_dir is None:
            print(f"Unable to find recipes meta directory in '{recipe_dir}'")
            return False

        _, recipe_name = os.path.split(recipe_dir)
        recipe_meta_dir = os.path.join(recipes_meta_dir, recipe_name)
        recipe_sha_file = os.path.join(recipe_meta_dir, FILE_SHA)

        contents = DKFileHelper.read_file(recipe_sha_file)
        new_contents = ""
        for line in contents.split("\n"):
            if line.startswith(os.path.join(recipe_name, file_recipe_path) + ":"):
                pass  # removes the line
            else:
                new_contents += f"{line}\n"
        new_contents = new_contents.strip("\n")
        DKFileHelper.write_file(recipe_sha_file, new_contents)

    @staticmethod
    def write_recipe_state_file_update(recipe_dir: str, file_recipe_path: str) -> Optional[bool]:
        kitchen_meta_dir = DKKitchenDisk.find_kitchen_meta_dir(recipe_dir)
        if kitchen_meta_dir is None:
            print(f"Unable to find kitchen meta directory in '{recipe_dir}'")
            return False
        recipes_meta_dir = DKKitchenDisk.get_recipes_meta_dir(kitchen_meta_dir)
        if recipes_meta_dir is None:
            print(f"Unable to find recipes meta directory in '{recipe_dir}'")
            return False

        _, recipe_name = os.path.split(recipe_dir)
        recipe_meta_dir = os.path.join(recipes_meta_dir, recipe_name)
        recipe_sha_file = os.path.join(recipe_meta_dir, FILE_SHA)

        contents = DKFileHelper.read_file(recipe_sha_file)
        new_contents = ""
        for line in contents.split("\n"):
            if line.startswith(os.path.join(recipe_name, file_recipe_path) + ":"):
                full_file_path = os.path.join(recipe_dir, file_recipe_path)
                the_sha = githash_by_file_name(full_file_path)
                the_path = os.path.join(recipe_name, file_recipe_path)
                new_contents += f"{the_path}:{the_sha}\n"
            else:
                new_contents += f"{line}\n"
        new_contents = new_contents.strip("\n")
        DKFileHelper.write_file(recipe_sha_file, new_contents)

    @staticmethod
    def write_recipe_state_recipe_delete(kitchen_dir: str, recipe_name: Optional[str]) -> None:
        kitchen_meta_dir = DKKitchenDisk.find_kitchen_meta_dir(kitchen_dir)
        recipes_meta_dir = DKKitchenDisk.get_recipes_meta_dir(kitchen_meta_dir)
        recipe_meta_dir = os.path.join(recipes_meta_dir, recipe_name)
        if os.path.isdir(recipe_meta_dir):
            try:
                shutil.rmtree(recipe_meta_dir)
            except OSError:
                print(f"Warning: Could not delete {recipe_meta_dir}")

    @staticmethod
    # UNUSED METHOD?
    def get_changed_files(start_dir, recipe_name):

        kitchen_meta_dir = DKKitchenDisk.find_kitchen_meta_dir(start_dir)
        if kitchen_meta_dir is None:
            print(f"Unable to find kitchen meta directory in '{start_dir}'")
            return False, None, None, None
        recipes_meta_dir = DKKitchenDisk.get_recipes_meta_dir(kitchen_meta_dir)
        if recipes_meta_dir is None:
            print(f"Unable to find recipes meta directory in '{start_dir}'")
            return False, None, None, None

        recipe_meta_dir = os.path.join(recipes_meta_dir, recipe_name)

        current_shas = DKRecipeDisk.fetch_shas(start_dir)

        saved_shas = DKRecipeDisk.load_saved_shas(recipe_meta_dir)

        if not saved_shas:
            return False, None, None, None

        current_paths = set(current_shas.keys())
        saved_paths = set(saved_shas.keys())

        common_paths = saved_paths & current_paths

        new_paths = current_paths - saved_paths
        removed_paths = saved_paths - current_paths

        changed_paths = [path for path in common_paths if current_shas[path] != saved_shas[path]]

        return True, new_paths, changed_paths, removed_paths

    @staticmethod
    def load_saved_shas(recipe_meta_dir: str) -> Optional[JSONData]:
        saved_shas = {}

        sha_file = os.path.join(recipe_meta_dir, FILE_SHA)

        if not os.path.isfile(sha_file):
            return None

        with open(sha_file, "r") as f:
            for line in f.readlines():
                path, line_sha = line.strip().split(":")
                saved_shas[path] = line_sha

        return saved_shas

    def fetch_shas(self, base_dir: str) -> JSONData:
        shas = self.do_fetch_shas(base_dir)
        parent_path, recipe_dir = os.path.split(base_dir)
        return {p[len(parent_path) + 1 :]: v for p, v in shas.items()}

    def do_fetch_shas(self, base_dir: str) -> JSONData:
        result = {}
        for item in [f for f in os.listdir(base_dir) if not self.ignore.ignore(f)]:
            item_path = os.path.join(base_dir, item)

            if os.path.isfile(item_path):
                result[item_path] = githash_by_file_name(item_path)
            elif os.path.isdir(item_path):
                result.update(self.do_fetch_shas(item_path))
        return result

    @staticmethod
    def get_orig_head(start_dir: str) -> Optional[str]:
        recipe_meta_dir = DKRecipeDisk.find_recipe_meta_dir(start_dir)
        if recipe_meta_dir is None:
            return None

        orig_head = os.path.join(recipe_meta_dir, ORIG_HEAD)
        if not os.path.exists(orig_head):
            return None

        try:
            orig_head = DKFileHelper.read_file(orig_head)
        except OSError as e:
            print(f"{e.filename} - {e.errno} - {e}")
            return None
        return orig_head

    @staticmethod
    def create_conflicts_meta(recipe_meta_dir: Optional[str]) -> str:
        conflicts_file_path = os.path.join(recipe_meta_dir, DK_CONFLICTS_META)
        if os.path.exists(conflicts_file_path):
            return conflicts_file_path
        else:
            DKFileHelper.write_file(conflicts_file_path, "{}")
            return conflicts_file_path

    @staticmethod
    def add_conflict_to_conflicts_meta(
        conflict_info: JSONData, folder_in_recipe: str, recipe_name: str, kitchen_dir: str
    ) -> bool:
        recipe_meta_dir = DKKitchenDisk.get_recipe_meta_dir(recipe_name, kitchen_dir)
        conflicts_meta = DKRecipeDisk.get_conflicts_meta(recipe_meta_dir)
        conflict_key = "{}|{}|{}|{}|{}".format(
            conflict_info["from_kitchen"],
            conflict_info["to_kitchen"],
            recipe_name,
            folder_in_recipe,
            conflict_info["filename"],
        )

        conflict_for_save = conflict_info.copy()
        conflict_for_save["folder_in_recipe"] = folder_in_recipe
        conflict_for_save["status"] = "unresolved"
        if folder_in_recipe not in conflicts_meta:
            conflicts_meta[folder_in_recipe] = {}
        conflicts_meta[folder_in_recipe][conflict_key] = conflict_for_save
        return DKRecipeDisk.save_conflicts_meta(recipe_meta_dir, conflicts_meta)

    @staticmethod
    def get_conflicts_meta(recipe_meta_dir: Optional[str]) -> JSONData:
        conflicts_file_path = os.path.join(recipe_meta_dir, DK_CONFLICTS_META)
        if not os.path.exists(conflicts_file_path):
            conflicts_file_path = DKRecipeDisk.create_conflicts_meta(recipe_meta_dir)

        with open(conflicts_file_path, "r") as conflicts_file:
            conflicts = json.load(conflicts_file)
        return conflicts

    @staticmethod
    # UNUSED METHOD?
    def get_unresolved_conflicts_meta(recipe_meta_dir, from_kitchen=None, to_kitchen=None):
        conflicts = DKRecipeDisk.get_conflicts_meta(recipe_meta_dir)
        unresolved_conflicts = {}
        for recipe_folder, folder_conflicts in six.iteritems(conflicts):
            for conflict_key, conflict_info in six.iteritems(folder_conflicts):
                if conflict_info["status"] == "unresolved":
                    add_it = True
                    if from_kitchen is not None and to_kitchen is not None:
                        if from_kitchen != conflict_info["from_kitchen"] or conflict_info["to_kitchen"] != to_kitchen:
                            add_it = False
                    if add_it:
                        if recipe_folder not in unresolved_conflicts:
                            unresolved_conflicts[recipe_folder] = {}
                        unresolved_conflicts[recipe_folder][conflict_key] = conflict_info
        return unresolved_conflicts

    @staticmethod
    # UNUSED METHOD?
    def get_resolved_conflicts_meta(recipe_meta_dir, from_kitchen=None, to_kitchen=None):
        conflicts = DKRecipeDisk.get_conflicts_meta(recipe_meta_dir)
        resolved_conflicts = {}
        for recipe_folder, folder_conflicts in six.iteritems(conflicts):
            for conflict_key, conflict_info in six.iteritems(folder_conflicts):
                if conflict_info["status"] == "resolved":
                    add_it = True
                    if from_kitchen is not None and to_kitchen is not None:
                        if from_kitchen != conflict_info["from_kitchen"] or conflict_info["to_kitchen"] != to_kitchen:
                            add_it = False
                    if add_it:
                        if recipe_folder not in resolved_conflicts:
                            resolved_conflicts[recipe_folder] = {}
                        resolved_conflicts[recipe_folder][conflict_key] = conflict_info
                    else:
                        print(
                            "Found a resolved conflict for from "
                            f"'{conflict_info['from_kitchen']}' to "
                            f"'{conflict_info['to_kitchen']}', "
                            "but we are looking for "
                            f"from '{from_kitchen}' to '{to_kitchen}'"
                        )
        return resolved_conflicts

    @staticmethod
    # UNUSED METHOD?
    def resolve_conflict(recipe_meta_dir, recipe_root_dir, file_path):
        all_conflicts = DKRecipeDisk.get_conflicts_meta(recipe_meta_dir)
        norm_file_path = os.path.normpath(file_path)
        local_path_in_recipe = norm_file_path.replace(recipe_root_dir, "")
        reg = re.compile(f"^{os.sep}|/$")
        local_path_in_recipe = re.sub(reg, "", local_path_in_recipe)
        recipe_name = DKRecipeDisk.find_recipe_name(recipe_root_dir)
        for recipe_folder, folder_contents in six.iteritems(all_conflicts):
            for conflict_key, conflict_info in six.iteritems(folder_contents):
                if conflict_info["status"] == "unresolved":
                    path_in_recipe = os.path.join(conflict_info["folder_in_recipe"], conflict_info["filename"])
                    reg = re.compile(f"{recipe_name}/")
                    path_in_recipe = re.sub(reg, "", path_in_recipe)
                    if local_path_in_recipe == path_in_recipe:
                        conflict_info["status"] = "resolved"
                        folder_contents[conflict_key] = conflict_info
                        DKRecipeDisk.save_conflicts_meta(recipe_meta_dir, all_conflicts)
                        return True
        return False

    @staticmethod
    def save_conflicts_meta(recipe_meta_dir: Optional[str], conflicts_meta: JSONData) -> bool:
        conflicts_file_path = os.path.join(recipe_meta_dir, DK_CONFLICTS_META)
        DKFileHelper.write_file(
            conflicts_file_path, json.dumps(conflicts_meta, sort_keys=True, indent=2, separators=(",", ": ")),
        )
        return True

    @staticmethod
    def _get_my_recipe_meta(kitchen_meta_dir: str, recipe_name: bytes) -> Optional[Union[str, bytes]]:
        recipe_meta_file_path = os.path.join(
            DKKitchenDisk.get_recipes_meta_dir(kitchen_meta_dir), recipe_name, RECIPE_META
        )
        if not os.path.isfile(recipe_meta_file_path):
            return None

        contents = DKFileHelper.read_file(recipe_meta_file_path)
        return contents

    @staticmethod
    def find_recipe_root_dir(check_dir: Optional[str] = None) -> Optional[str]:
        return DKRecipeDisk._find_recipe(check_dir, return_recipe_root_path=True)

    @staticmethod
    def find_recipe_meta_dir(check_dir: Optional[str] = None) -> Union[None, str, bool]:
        recipe_root_dir = DKRecipeDisk.find_recipe_root_dir(check_dir)
        if recipe_root_dir is None:
            return None

        recipe_name = DKRecipeDisk.find_recipe_name(recipe_root_dir)
        if recipe_name is None:
            return None

        kitchen_meta_dir = DKKitchenDisk.find_kitchen_meta_dir(recipe_root_dir)
        if kitchen_meta_dir is None:
            print(f"Unable to find kitchen meta directory in '{check_dir}'")
            return False

        recipes_meta_dir = DKKitchenDisk.get_recipes_meta_dir(kitchen_meta_dir)
        if recipes_meta_dir is None:
            print(f"Unable to find recipes meta directory in '{check_dir}'")
            return False

        recipe_meta_dir = os.path.join(recipes_meta_dir, recipe_name)
        return recipe_meta_dir

    @staticmethod
    def is_recipe_root_dir(check_dir: Optional[str] = None) -> bool:
        found_path = DKRecipeDisk._find_recipe(check_dir, return_recipe_root_path=True)
        if found_path == check_dir:
            return True
        else:
            return False

    @staticmethod
    def find_recipe_name(walk_dir: Optional[str] = None) -> Optional[str]:
        return DKRecipeDisk._find_recipe(walk_dir)

    @staticmethod
    def _find_recipe(walk_dir: Optional[str] = None, return_recipe_root_path: bool = False) -> Optional[str]:

        if walk_dir is None:
            walk_dir = os.getcwd()

        kitchen_meta_dir = DKKitchenDisk.find_kitchen_meta_dir(walk_dir)
        if kitchen_meta_dir is None:
            # We aren't in a kitchen folder.
            return None

        kitchen_root_dir = DKKitchenDisk.find_kitchen_root_dir(walk_dir)
        if kitchen_root_dir is None:
            # We aren't in a kitchen folder.
            return None

        if walk_dir == kitchen_root_dir or walk_dir == kitchen_meta_dir:
            # We are in the kitchen root folder. Can't do anything here.
            return None

        current_dir_abs = os.path.abspath(walk_dir)
        kitchen_root_dir_abs = os.path.abspath(kitchen_root_dir)

        common = os.path.commonprefix([current_dir_abs, kitchen_root_dir_abs])
        current_dir_relative = current_dir_abs.replace(common + os.sep, "")
        parts = current_dir_relative.split(os.sep)
        if len(parts) == 0:
            # Looks like we are in the kitchen folder.
            return None

        recipe_name = parts[0]
        recipe_meta_contents = DKRecipeDisk._get_my_recipe_meta(kitchen_meta_dir, recipe_name)
        if recipe_name == recipe_meta_contents:
            if not return_recipe_root_path:
                return recipe_name
            else:
                return os.path.join(kitchen_root_dir, recipe_name)
        else:
            return None

    @staticmethod
    # UNUSED METHOD?
    def sort_file(list_of_files):

        # sorted_files = dict()
        # for this_file in list_of_files:
        #    file_name = this_file
        return list_of_files

    @staticmethod
    def write_files(full_dir: str, file_dict: JSONData, format: bool = False) -> None:
        if "filename" in file_dict:
            abspath = os.path.join(full_dir, file_dict["filename"])

            if "json" in file_dict:
                if isinstance(file_dict["json"], dict) is True:
                    if format:
                        json_str = json.dumps(file_dict["json"], indent=4, separators=(",", ": "))
                    else:
                        json_str = json.dumps(file_dict["json"])
                    DKFileHelper.write_file(abspath, json_str)
                else:
                    DKFileHelper.write_file(abspath, file_dict["json"].encode("utf8"))
            elif "text" in file_dict:
                text = file_dict["text"]
                DKFileHelper.write_file(abspath, text)


# http://stackoverflow.com/questions/4187564/recursive-dircmp-compare-two-directories-to-ensure-they-have-the-same-files-and
class dircmp(filecmp.dircmp):
    """
    Compare the content of dir1 and dir2. In contrast with filecmp.dircmp, this
    subclass compares the content of files with the same path.
    """

    def phase3(self) -> None:
        """
        Find out differences between common files.
        Ensure we are using content comparison with shallow=False.
        """
        fcomp = filecmp.cmpfiles(self.left, self.right, self.common_files, shallow=False)
        self.same_files, self.diff_files, self.funny_files = fcomp


def compare_sha(
    ignore: DKIgnore,
    remote_sha: JSONData,
    local_sha: JSONData,
    start_dir: Optional[str] = None,
    recipe: Optional[str] = None,
) -> JSONData:
    same = dict()
    different = dict()
    local_modified = dict()
    remote_modified = dict()
    local_and_remote_modified = dict()
    non_local_modified = dict()
    only_local = dict()
    only_local_dir = dict()
    only_remote = dict()
    only_remote_dir = dict()
    saved_shas = None
    # Look for differences from remote
    for remote_path in remote_sha:
        for remote_file in remote_sha[remote_path]:
            if remote_path in local_sha:
                local_files_found = [
                    local_file
                    for local_file in local_sha[remote_path]
                    if local_file["filename"] == remote_file["filename"]
                ]
            else:
                if remote_path not in only_remote_dir:
                    only_remote_dir[remote_path] = list()
                local_files_found = list()
            if len(local_files_found) != 0:
                if local_files_found[0]["sha"] == remote_file["sha"]:
                    if remote_path not in same:
                        same[remote_path] = list()
                    same[remote_path].append(remote_file)
                else:  # local sha != remote sha
                    if remote_path not in different:
                        different[remote_path] = list()
                    different[remote_path].append(remote_file)

                    # check if file is modified local only, or both local and remote
                    if not saved_shas:
                        kitchen_meta_dir = DKKitchenDisk.find_kitchen_meta_dir(start_dir)
                        recipes_meta_dir = DKKitchenDisk.get_recipes_meta_dir(kitchen_meta_dir)
                        recipe_meta_dir = os.path.join(recipes_meta_dir, recipe)
                        saved_shas = DKRecipeDisk.load_saved_shas(recipe_meta_dir)
                    file_path = str(os.path.join(remote_path, remote_file["filename"]))
                    saved_sha = saved_shas[file_path]
                    if saved_sha == remote_file["sha"]:  # file is modified locally only
                        if remote_path not in local_modified:
                            local_modified[remote_path] = list()
                        local_modified[remote_path].append(remote_file)
                    elif saved_sha == local_files_found[0]["sha"]:  # file is modified remotely only
                        if remote_path not in remote_modified:
                            remote_modified[remote_path] = list()
                        remote_modified[remote_path].append(remote_file)
                        if remote_path not in non_local_modified:
                            non_local_modified[remote_path] = list()
                        non_local_modified[remote_path].append(remote_file)
                    else:  # file is modified both locally and remotely
                        if remote_path not in local_and_remote_modified:
                            local_and_remote_modified[remote_path] = list()
                        local_and_remote_modified[remote_path].append(remote_file)
                        if remote_path not in non_local_modified:
                            non_local_modified[remote_path] = list()
                        non_local_modified[remote_path].append(remote_file)

            elif len(local_files_found) > 1:
                raise Exception("compare_sha: Unexpected return in remote_path")
            else:
                if remote_path not in only_remote:
                    only_remote[remote_path] = list()
                only_remote[remote_path].append(remote_file)

    for local_path, local_files in six.iteritems(local_sha):
        if ignore.ignore(local_path):
            # Ignore some stuff.
            continue
        elif local_path in remote_sha:
            for local_file in local_files:
                if ignore.ignore(local_file["filename"]):
                    continue
                elif ignore.ignore(os.path.join(local_path, local_file["filename"])):
                    continue
                remote_files_found = [
                    remote_file
                    for remote_file in remote_sha[local_path]
                    if remote_file["filename"] == local_file["filename"]
                ]

                if len(remote_files_found) > 1:
                    raise Exception("compare_sha: Unexpected return in remote_path")
                elif len(remote_files_found) == 0:
                    if local_path not in only_local:
                        only_local[local_path] = list()
                    only_local[local_path].append(local_file)
        else:
            if local_path not in only_local:
                only_local_dir[local_path] = list()
                only_local[local_path] = list()
                for local_file in local_files:
                    only_local[local_path].append(local_file)

    rv = dict()
    rv["same"] = same
    rv["different"] = different
    rv["local_modified"] = local_modified
    rv["remote_modified"] = remote_modified
    rv["local_and_remote_modified"] = local_and_remote_modified
    rv["non_local_modified"] = non_local_modified
    rv["only_local"] = only_local
    rv["only_local_dir"] = only_local_dir
    rv["only_remote"] = only_remote
    rv["only_remote_dir"] = only_remote_dir
    return rv


def get_directory_sha(ignore: DKIgnore, walk_dir: str) -> JSONData:
    recipe_name = os.path.basename(walk_dir)
    rootdir = os.path.dirname(walk_dir)
    r = dict()
    r[recipe_name] = []
    for root, subdirs, files in os.walk(walk_dir):
        for filename in files:
            if not ignore.ignore(filename):
                file_path = os.path.join(root, filename)
                part = file_path.split(rootdir, 1)[1]
                part2 = part.split(filename, 1)[0]
                part3 = part2[1:-1]
                r[part3].append({"filename": filename, "sha": githash_by_file_name(file_path)})
        for subdir in subdirs:
            subdir_fullpath = os.path.join(root, subdir)
            part = subdir_fullpath.split(rootdir, 1)[1]
            part2 = part[1:]
            r[part2] = []
    return r
