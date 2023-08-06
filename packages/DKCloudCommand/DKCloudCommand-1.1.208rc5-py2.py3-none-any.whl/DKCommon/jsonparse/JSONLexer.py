# Generated from JSON.g by ANTLR 4.7.1
# encoding: utf-8
from __future__ import print_function

import sys

from antlr4 import (
    ATNDeserializer,
    DFA,
    Lexer,
    LexerATNSimulator,
    PredictionContextCache,
)
from io import StringIO


def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2")
        buf.write(u"\16\u0082\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6")
        buf.write(u"\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4")
        buf.write(u"\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t")
        buf.write(u"\22\4\23\t\23\3\2\3\2\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3\6")
        buf.write(u"\3\7\3\7\3\b\3\b\3\b\3\b\3\b\3\t\3\t\3\t\3\t\3\t\3\t")
        buf.write(u"\3\n\3\n\3\n\3\n\3\n\3\13\3\13\3\13\7\13G\n\13\f\13\16")
        buf.write(u"\13J\13\13\3\13\3\13\3\f\3\f\3\f\5\fQ\n\f\3\r\3\r\3\r")
        buf.write(u"\3\r\3\r\3\r\3\16\3\16\3\17\3\17\3\20\5\20^\n\20\3\20")
        buf.write(u"\3\20\3\20\6\20c\n\20\r\20\16\20d\5\20g\n\20\3\20\5\20")
        buf.write(u"j\n\20\3\21\3\21\3\21\7\21o\n\21\f\21\16\21r\13\21\5")
        buf.write(u"\21t\n\21\3\22\3\22\5\22x\n\22\3\22\3\22\3\23\6\23}\n")
        buf.write(u"\23\r\23\16\23~\3\23\3\23\2\2\24\3\3\5\4\7\5\t\6\13\7")
        buf.write(u"\r\b\17\t\21\n\23\13\25\f\27\2\31\2\33\2\35\2\37\r!\2")
        buf.write(u"#\2%\16\3\2\n\n\2$$\61\61^^ddhhppttvv\5\2\62;CHch\5\2")
        buf.write(u"\2!$$^^\3\2\62;\3\2\63;\4\2GGgg\4\2--//\5\2\13\f\17\17")
        buf.write(u'""\2\u0086\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t')
        buf.write(u"\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3")
        buf.write(u"\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\37\3\2\2\2\2%\3\2")
        buf.write(u"\2\2\3'\3\2\2\2\5)\3\2\2\2\7+\3\2\2\2\t-\3\2\2\2\13")
        buf.write(u"/\3\2\2\2\r\61\3\2\2\2\17\63\3\2\2\2\218\3\2\2\2\23>")
        buf.write(u"\3\2\2\2\25C\3\2\2\2\27M\3\2\2\2\31R\3\2\2\2\33X\3\2")
        buf.write(u"\2\2\35Z\3\2\2\2\37]\3\2\2\2!s\3\2\2\2#u\3\2\2\2%|\3")
        buf.write(u"\2\2\2'(\7}\2\2(\4\3\2\2\2)*\7.\2\2*\6\3\2\2\2+,\7\177")
        buf.write(u"\2\2,\b\3\2\2\2-.\7<\2\2.\n\3\2\2\2/\60\7]\2\2\60\f\3")
        buf.write(u"\2\2\2\61\62\7_\2\2\62\16\3\2\2\2\63\64\7v\2\2\64\65")
        buf.write(u"\7t\2\2\65\66\7w\2\2\66\67\7g\2\2\67\20\3\2\2\289\7h")
        buf.write(u"\2\29:\7c\2\2:;\7n\2\2;<\7u\2\2<=\7g\2\2=\22\3\2\2\2")
        buf.write(u">?\7p\2\2?@\7w\2\2@A\7n\2\2AB\7n\2\2B\24\3\2\2\2CH\7")
        buf.write(u"$\2\2DG\5\27\f\2EG\5\35\17\2FD\3\2\2\2FE\3\2\2\2GJ\3")
        buf.write(u"\2\2\2HF\3\2\2\2HI\3\2\2\2IK\3\2\2\2JH\3\2\2\2KL\7$\2")
        buf.write(u"\2L\26\3\2\2\2MP\7^\2\2NQ\t\2\2\2OQ\5\31\r\2PN\3\2\2")
        buf.write(u"\2PO\3\2\2\2Q\30\3\2\2\2RS\7w\2\2ST\5\33\16\2TU\5\33")
        buf.write(u"\16\2UV\5\33\16\2VW\5\33\16\2W\32\3\2\2\2XY\t\3\2\2Y")
        buf.write(u"\34\3\2\2\2Z[\n\4\2\2[\36\3\2\2\2\\^\7/\2\2]\\\3\2\2")
        buf.write(u"\2]^\3\2\2\2^_\3\2\2\2_f\5!\21\2`b\7\60\2\2ac\t\5\2\2")
        buf.write(u"ba\3\2\2\2cd\3\2\2\2db\3\2\2\2de\3\2\2\2eg\3\2\2\2f`")
        buf.write(u"\3\2\2\2fg\3\2\2\2gi\3\2\2\2hj\5#\22\2ih\3\2\2\2ij\3")
        buf.write(u"\2\2\2j \3\2\2\2kt\7\62\2\2lp\t\6\2\2mo\t\5\2\2nm\3\2")
        buf.write(u"\2\2or\3\2\2\2pn\3\2\2\2pq\3\2\2\2qt\3\2\2\2rp\3\2\2")
        buf.write(u'\2sk\3\2\2\2sl\3\2\2\2t"\3\2\2\2uw\t\7\2\2vx\t\b\2\2')
        buf.write(u"wv\3\2\2\2wx\3\2\2\2xy\3\2\2\2yz\5!\21\2z$\3\2\2\2{}")
        buf.write(u"\t\t\2\2|{\3\2\2\2}~\3\2\2\2~|\3\2\2\2~\177\3\2\2\2\177")
        buf.write(u"\u0080\3\2\2\2\u0080\u0081\b\23\2\2\u0081&\3\2\2\2\16")
        buf.write(u"\2FHP]dfipsw~\3\b\2\2")
        return buf.getvalue()


class JSONLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    STRING = 10
    NUMBER = 11
    WS = 12

    channelNames = [u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN"]

    modeNames = [u"DEFAULT_MODE"]

    literalNames = [
        u"<INVALID>",
        u"'{'",
        u"','",
        u"'}'",
        u"':'",
        u"'['",
        u"']'",
        u"'true'",
        u"'false'",
        u"'null'",
    ]

    symbolicNames = [u"<INVALID>", u"STRING", u"NUMBER", u"WS"]

    ruleNames = [
        u"T__0",
        u"T__1",
        u"T__2",
        u"T__3",
        u"T__4",
        u"T__5",
        u"T__6",
        u"T__7",
        u"T__8",
        u"STRING",
        u"ESC",
        u"UNICODE",
        u"HEX",
        u"SAFECODEPOINT",
        u"NUMBER",
        u"INT",
        u"EXP",
        u"WS",
    ]

    grammarFileName = u"JSON.g"

    def __init__(self, input=None, output=sys.stdout):
        super(JSONLexer, self).__init__(input, output=output)
        self.checkVersion("4.7.1")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None
