from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\27")
        buf.write("\u0096\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\3\2\3\2\5\2\60\n\2")
        buf.write("\3\3\3\3\3\3\3\3\3\4\3\4\3\4\3\5\3\5\3\5\3\5\3\6\3\6\3")
        buf.write("\6\3\6\3\6\3\7\3\7\3\7\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\b")
        buf.write("\3\t\3\t\3\n\3\n\3\n\3\13\3\13\3\f\3\f\3\f\3\r\3\r\3\r")
        buf.write("\3\16\3\16\3\16\3\17\3\17\3\20\3\20\3\21\3\21\3\21\3\21")
        buf.write("\3\22\5\22f\n\22\3\22\6\22i\n\22\r\22\16\22j\3\22\3\22")
        buf.write("\6\22o\n\22\r\22\16\22p\5\22s\n\22\3\23\3\23\3\23\3\23")
        buf.write("\7\23y\n\23\f\23\16\23|\13\23\3\23\3\23\3\24\3\24\7\24")
        buf.write("\u0082\n\24\f\24\16\24\u0085\13\24\3\25\3\25\3\25\6\25")
        buf.write("\u008a\n\25\r\25\16\25\u008b\3\25\3\25\3\26\6\26\u0091")
        buf.write("\n\26\r\26\16\26\u0092\3\26\3\26\2\2\27\3\3\5\4\7\5\t")
        buf.write("\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20")
        buf.write("\37\21!\22#\23%\24\'\25)\26+\27\3\2\b\3\2\62;\6\2\f\f")
        buf.write("\17\17$$^^\4\2$$^^\5\2C\\aac|\7\2\60\60\62;C\\aac|\5\2")
        buf.write("\13\f\16\17\"\"\2\u009f\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3")
        buf.write("\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2")
        buf.write("\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2")
        buf.write("\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2")
        buf.write("!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2")
        buf.write("\2+\3\2\2\2\3/\3\2\2\2\5\61\3\2\2\2\7\65\3\2\2\2\t8\3")
        buf.write("\2\2\2\13<\3\2\2\2\rA\3\2\2\2\17G\3\2\2\2\21L\3\2\2\2")
        buf.write("\23N\3\2\2\2\25Q\3\2\2\2\27S\3\2\2\2\31V\3\2\2\2\33Y\3")
        buf.write("\2\2\2\35\\\3\2\2\2\37^\3\2\2\2!`\3\2\2\2#e\3\2\2\2%t")
        buf.write("\3\2\2\2\'\177\3\2\2\2)\u0086\3\2\2\2+\u0090\3\2\2\2-")
        buf.write("\60\5\13\6\2.\60\5\r\7\2/-\3\2\2\2/.\3\2\2\2\60\4\3\2")
        buf.write("\2\2\61\62\7C\2\2\62\63\7P\2\2\63\64\7F\2\2\64\6\3\2\2")
        buf.write("\2\65\66\7Q\2\2\66\67\7T\2\2\67\b\3\2\2\289\7P\2\29:\7")
        buf.write("Q\2\2:;\7V\2\2;\n\3\2\2\2<=\7v\2\2=>\7t\2\2>?\7w\2\2?")
        buf.write("@\7g\2\2@\f\3\2\2\2AB\7h\2\2BC\7c\2\2CD\7n\2\2DE\7u\2")
        buf.write("\2EF\7g\2\2F\16\3\2\2\2GH\7p\2\2HI\7w\2\2IJ\7n\2\2JK\7")
        buf.write("n\2\2K\20\3\2\2\2LM\7@\2\2M\22\3\2\2\2NO\7@\2\2OP\7?\2")
        buf.write("\2P\24\3\2\2\2QR\7>\2\2R\26\3\2\2\2ST\7>\2\2TU\7?\2\2")
        buf.write("U\30\3\2\2\2VW\7?\2\2WX\7?\2\2X\32\3\2\2\2YZ\7#\2\2Z[")
        buf.write("\7?\2\2[\34\3\2\2\2\\]\7*\2\2]\36\3\2\2\2^_\7+\2\2_ \3")
        buf.write("\2\2\2`a\7)\2\2ab\13\2\2\2bc\7)\2\2c\"\3\2\2\2df\7/\2")
        buf.write("\2ed\3\2\2\2ef\3\2\2\2fh\3\2\2\2gi\t\2\2\2hg\3\2\2\2i")
        buf.write("j\3\2\2\2jh\3\2\2\2jk\3\2\2\2kr\3\2\2\2ln\7\60\2\2mo\t")
        buf.write("\2\2\2nm\3\2\2\2op\3\2\2\2pn\3\2\2\2pq\3\2\2\2qs\3\2\2")
        buf.write("\2rl\3\2\2\2rs\3\2\2\2s$\3\2\2\2tz\7$\2\2uy\n\3\2\2vw")
        buf.write("\7^\2\2wy\t\4\2\2xu\3\2\2\2xv\3\2\2\2y|\3\2\2\2zx\3\2")
        buf.write("\2\2z{\3\2\2\2{}\3\2\2\2|z\3\2\2\2}~\7$\2\2~&\3\2\2\2")
        buf.write("\177\u0083\t\5\2\2\u0080\u0082\t\6\2\2\u0081\u0080\3\2")
        buf.write("\2\2\u0082\u0085\3\2\2\2\u0083\u0081\3\2\2\2\u0083\u0084")
        buf.write("\3\2\2\2\u0084(\3\2\2\2\u0085\u0083\3\2\2\2\u0086\u0087")
        buf.write("\7&\2\2\u0087\u0089\7}\2\2\u0088\u008a\t\6\2\2\u0089\u0088")
        buf.write("\3\2\2\2\u008a\u008b\3\2\2\2\u008b\u0089\3\2\2\2\u008b")
        buf.write("\u008c\3\2\2\2\u008c\u008d\3\2\2\2\u008d\u008e\7\177\2")
        buf.write("\2\u008e*\3\2\2\2\u008f\u0091\t\7\2\2\u0090\u008f\3\2")
        buf.write("\2\2\u0091\u0092\3\2\2\2\u0092\u0090\3\2\2\2\u0092\u0093")
        buf.write("\3\2\2\2\u0093\u0094\3\2\2\2\u0094\u0095\b\26\2\2\u0095")
        buf.write(",\3\2\2\2\r\2/ejprxz\u0083\u008b\u0092\3\b\2\2")
        return buf.getvalue()


class ConditionLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    BOOLEAN = 1
    AND = 2
    OR = 3
    NOT = 4
    TRUE = 5
    FALSE = 6
    NULL = 7
    GT = 8
    GE = 9
    LT = 10
    LE = 11
    EQ = 12
    NE = 13
    LPAREN = 14
    RPAREN = 15
    CHARACTER = 16
    NUMBER = 17
    STRING = 18
    VARIABLE = 19
    PLACEHOLDER = 20
    WS = 21

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'AND'", "'OR'", "'NOT'", "'true'", "'false'", "'null'", "'>'", 
            "'>='", "'<'", "'<='", "'=='", "'!='", "'('", "')'" ]

    symbolicNames = [ "<INVALID>",
            "BOOLEAN", "AND", "OR", "NOT", "TRUE", "FALSE", "NULL", "GT", 
            "GE", "LT", "LE", "EQ", "NE", "LPAREN", "RPAREN", "CHARACTER", 
            "NUMBER", "STRING", "VARIABLE", "PLACEHOLDER", "WS" ]

    ruleNames = [ "BOOLEAN", "AND", "OR", "NOT", "TRUE", "FALSE", "NULL", 
                  "GT", "GE", "LT", "LE", "EQ", "NE", "LPAREN", "RPAREN", 
                  "CHARACTER", "NUMBER", "STRING", "VARIABLE", "PLACEHOLDER", 
                  "WS" ]

    grammarFileName = "Condition.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


