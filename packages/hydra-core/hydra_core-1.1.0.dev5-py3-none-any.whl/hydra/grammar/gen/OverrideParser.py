# Generated from /home/omry/dev/hydra/hydra/grammar/OverrideParser.g4 by ANTLR 4.8
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\32")
        buf.write("\u00a3\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\3\2\3\2\3\2\5\2\"\n\2\3\2\3\2\3\2\3\2")
        buf.write("\5\2(\n\2\5\2*\n\2\3\2\3\2\5\2.\n\2\3\2\3\2\3\2\5\2\63")
        buf.write("\n\2\5\2\65\n\2\3\2\3\2\3\3\3\3\3\3\5\3<\n\3\3\4\3\4\3")
        buf.write("\4\3\4\6\4B\n\4\r\4\16\4C\5\4F\n\4\3\5\3\5\3\5\5\5K\n")
        buf.write("\5\3\6\3\6\5\6O\n\6\3\7\3\7\3\7\3\7\5\7U\n\7\3\b\3\b\3")
        buf.write("\b\6\bZ\n\b\r\b\16\b[\3\t\3\t\3\t\3\n\3\n\3\n\5\nd\n\n")
        buf.write("\3\n\3\n\3\n\5\ni\n\n\3\n\7\nl\n\n\f\n\16\no\13\n\5\n")
        buf.write("q\n\n\3\n\3\n\3\13\3\13\3\13\3\13\7\13y\n\13\f\13\16\13")
        buf.write("|\13\13\5\13~\n\13\3\13\3\13\3\f\3\f\3\f\3\f\7\f\u0086")
        buf.write("\n\f\f\f\16\f\u0089\13\f\5\f\u008b\n\f\3\f\3\f\3\r\3\r")
        buf.write("\3\r\3\r\3\16\3\16\6\16\u0095\n\16\r\16\16\16\u0096\5")
        buf.write("\16\u0099\n\16\3\17\3\17\6\17\u009d\n\17\r\17\16\17\u009e")
        buf.write("\5\17\u00a1\n\17\3\17\2\2\20\2\4\6\b\n\f\16\20\22\24\26")
        buf.write("\30\32\34\2\4\5\2\7\7\21\30\32\32\3\2\21\30\2\u00b1\2")
        buf.write("\64\3\2\2\2\48\3\2\2\2\6E\3\2\2\2\bJ\3\2\2\2\nN\3\2\2")
        buf.write("\2\fT\3\2\2\2\16V\3\2\2\2\20]\3\2\2\2\22`\3\2\2\2\24t")
        buf.write("\3\2\2\2\26\u0081\3\2\2\2\30\u008e\3\2\2\2\32\u0098\3")
        buf.write("\2\2\2\34\u00a0\3\2\2\2\36\37\5\4\3\2\37!\7\3\2\2 \"\5")
        buf.write("\n\6\2! \3\2\2\2!\"\3\2\2\2\"\65\3\2\2\2#$\7\4\2\2$)\5")
        buf.write("\4\3\2%\'\7\3\2\2&(\5\n\6\2\'&\3\2\2\2\'(\3\2\2\2(*\3")
        buf.write("\2\2\2)%\3\2\2\2)*\3\2\2\2*\65\3\2\2\2+-\7\5\2\2,.\7\5")
        buf.write("\2\2-,\3\2\2\2-.\3\2\2\2./\3\2\2\2/\60\5\4\3\2\60\62\7")
        buf.write("\3\2\2\61\63\5\n\6\2\62\61\3\2\2\2\62\63\3\2\2\2\63\65")
        buf.write("\3\2\2\2\64\36\3\2\2\2\64#\3\2\2\2\64+\3\2\2\2\65\66\3")
        buf.write("\2\2\2\66\67\7\2\2\3\67\3\3\2\2\28;\5\6\4\29:\7\6\2\2")
        buf.write(":<\5\b\5\2;9\3\2\2\2;<\3\2\2\2<\5\3\2\2\2=F\5\b\5\2>A")
        buf.write("\7\26\2\2?@\7\b\2\2@B\7\26\2\2A?\3\2\2\2BC\3\2\2\2CA\3")
        buf.write("\2\2\2CD\3\2\2\2DF\3\2\2\2E=\3\2\2\2E>\3\2\2\2F\7\3\2")
        buf.write("\2\2GK\3\2\2\2HK\7\26\2\2IK\7\t\2\2JG\3\2\2\2JH\3\2\2")
        buf.write("\2JI\3\2\2\2K\t\3\2\2\2LO\5\f\7\2MO\5\16\b\2NL\3\2\2\2")
        buf.write("NM\3\2\2\2O\13\3\2\2\2PU\5\32\16\2QU\5\24\13\2RU\5\26")
        buf.write("\f\2SU\5\22\n\2TP\3\2\2\2TQ\3\2\2\2TR\3\2\2\2TS\3\2\2")
        buf.write("\2U\r\3\2\2\2VY\5\f\7\2WX\7\13\2\2XZ\5\f\7\2YW\3\2\2\2")
        buf.write("Z[\3\2\2\2[Y\3\2\2\2[\\\3\2\2\2\\\17\3\2\2\2]^\7\26\2")
        buf.write("\2^_\7\3\2\2_\21\3\2\2\2`a\7\26\2\2ap\7\n\2\2bd\5\20\t")
        buf.write("\2cb\3\2\2\2cd\3\2\2\2de\3\2\2\2em\5\f\7\2fh\7\13\2\2")
        buf.write("gi\5\20\t\2hg\3\2\2\2hi\3\2\2\2ij\3\2\2\2jl\5\f\7\2kf")
        buf.write("\3\2\2\2lo\3\2\2\2mk\3\2\2\2mn\3\2\2\2nq\3\2\2\2om\3\2")
        buf.write("\2\2pc\3\2\2\2pq\3\2\2\2qr\3\2\2\2rs\7\f\2\2s\23\3\2\2")
        buf.write("\2t}\7\r\2\2uz\5\f\7\2vw\7\13\2\2wy\5\f\7\2xv\3\2\2\2")
        buf.write("y|\3\2\2\2zx\3\2\2\2z{\3\2\2\2{~\3\2\2\2|z\3\2\2\2}u\3")
        buf.write("\2\2\2}~\3\2\2\2~\177\3\2\2\2\177\u0080\7\16\2\2\u0080")
        buf.write("\25\3\2\2\2\u0081\u008a\7\17\2\2\u0082\u0087\5\30\r\2")
        buf.write("\u0083\u0084\7\13\2\2\u0084\u0086\5\30\r\2\u0085\u0083")
        buf.write("\3\2\2\2\u0086\u0089\3\2\2\2\u0087\u0085\3\2\2\2\u0087")
        buf.write("\u0088\3\2\2\2\u0088\u008b\3\2\2\2\u0089\u0087\3\2\2\2")
        buf.write("\u008a\u0082\3\2\2\2\u008a\u008b\3\2\2\2\u008b\u008c\3")
        buf.write("\2\2\2\u008c\u008d\7\20\2\2\u008d\27\3\2\2\2\u008e\u008f")
        buf.write("\5\34\17\2\u008f\u0090\7\7\2\2\u0090\u0091\5\f\7\2\u0091")
        buf.write("\31\3\2\2\2\u0092\u0099\7\31\2\2\u0093\u0095\t\2\2\2\u0094")
        buf.write("\u0093\3\2\2\2\u0095\u0096\3\2\2\2\u0096\u0094\3\2\2\2")
        buf.write("\u0096\u0097\3\2\2\2\u0097\u0099\3\2\2\2\u0098\u0092\3")
        buf.write("\2\2\2\u0098\u0094\3\2\2\2\u0099\33\3\2\2\2\u009a\u00a1")
        buf.write("\7\31\2\2\u009b\u009d\t\3\2\2\u009c\u009b\3\2\2\2\u009d")
        buf.write("\u009e\3\2\2\2\u009e\u009c\3\2\2\2\u009e\u009f\3\2\2\2")
        buf.write("\u009f\u00a1\3\2\2\2\u00a0\u009a\3\2\2\2\u00a0\u009c\3")
        buf.write("\2\2\2\u00a1\35\3\2\2\2\33!\')-\62\64;CEJNT[chmpz}\u0087")
        buf.write("\u008a\u0096\u0098\u009e\u00a0")
        return buf.getvalue()


class OverrideParser ( Parser ):

    grammarFileName = "OverrideParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "'~'", "'+'", "'@'", "':'", 
                     "'/'" ]

    symbolicNames = [ "<INVALID>", "EQUAL", "TILDE", "PLUS", "AT", "COLON", 
                      "SLASH", "DOT_PATH", "POPEN", "COMMA", "PCLOSE", "BRACKET_OPEN", 
                      "BRACKET_CLOSE", "BRACE_OPEN", "BRACE_CLOSE", "FLOAT", 
                      "INT", "BOOL", "NULL", "UNQUOTED_CHAR", "ID", "ESC", 
                      "WS", "QUOTED_VALUE", "INTERPOLATION" ]

    RULE_override = 0
    RULE_key = 1
    RULE_packageOrGroup = 2
    RULE_package = 3
    RULE_value = 4
    RULE_element = 5
    RULE_simpleChoiceSweep = 6
    RULE_argName = 7
    RULE_function = 8
    RULE_listContainer = 9
    RULE_dictContainer = 10
    RULE_dictKeyValuePair = 11
    RULE_primitive = 12
    RULE_dictKey = 13

    ruleNames =  [ "override", "key", "packageOrGroup", "package", "value", 
                   "element", "simpleChoiceSweep", "argName", "function", 
                   "listContainer", "dictContainer", "dictKeyValuePair", 
                   "primitive", "dictKey" ]

    EOF = Token.EOF
    EQUAL=1
    TILDE=2
    PLUS=3
    AT=4
    COLON=5
    SLASH=6
    DOT_PATH=7
    POPEN=8
    COMMA=9
    PCLOSE=10
    BRACKET_OPEN=11
    BRACKET_CLOSE=12
    BRACE_OPEN=13
    BRACE_CLOSE=14
    FLOAT=15
    INT=16
    BOOL=17
    NULL=18
    UNQUOTED_CHAR=19
    ID=20
    ESC=21
    WS=22
    QUOTED_VALUE=23
    INTERPOLATION=24

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class OverrideContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(OverrideParser.EOF, 0)

        def key(self):
            return self.getTypedRuleContext(OverrideParser.KeyContext,0)


        def EQUAL(self):
            return self.getToken(OverrideParser.EQUAL, 0)

        def TILDE(self):
            return self.getToken(OverrideParser.TILDE, 0)

        def PLUS(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.PLUS)
            else:
                return self.getToken(OverrideParser.PLUS, i)

        def value(self):
            return self.getTypedRuleContext(OverrideParser.ValueContext,0)


        def getRuleIndex(self):
            return OverrideParser.RULE_override

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOverride" ):
                listener.enterOverride(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOverride" ):
                listener.exitOverride(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOverride" ):
                return visitor.visitOverride(self)
            else:
                return visitor.visitChildren(self)




    def override(self):

        localctx = OverrideParser.OverrideContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_override)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 50
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [OverrideParser.EQUAL, OverrideParser.AT, OverrideParser.DOT_PATH, OverrideParser.ID]:
                self.state = 28
                self.key()
                self.state = 29
                self.match(OverrideParser.EQUAL)
                self.state = 31
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << OverrideParser.COLON) | (1 << OverrideParser.BRACKET_OPEN) | (1 << OverrideParser.BRACE_OPEN) | (1 << OverrideParser.FLOAT) | (1 << OverrideParser.INT) | (1 << OverrideParser.BOOL) | (1 << OverrideParser.NULL) | (1 << OverrideParser.UNQUOTED_CHAR) | (1 << OverrideParser.ID) | (1 << OverrideParser.ESC) | (1 << OverrideParser.WS) | (1 << OverrideParser.QUOTED_VALUE) | (1 << OverrideParser.INTERPOLATION))) != 0):
                    self.state = 30
                    self.value()


                pass
            elif token in [OverrideParser.TILDE]:
                self.state = 33
                self.match(OverrideParser.TILDE)
                self.state = 34
                self.key()
                self.state = 39
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==OverrideParser.EQUAL:
                    self.state = 35
                    self.match(OverrideParser.EQUAL)
                    self.state = 37
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << OverrideParser.COLON) | (1 << OverrideParser.BRACKET_OPEN) | (1 << OverrideParser.BRACE_OPEN) | (1 << OverrideParser.FLOAT) | (1 << OverrideParser.INT) | (1 << OverrideParser.BOOL) | (1 << OverrideParser.NULL) | (1 << OverrideParser.UNQUOTED_CHAR) | (1 << OverrideParser.ID) | (1 << OverrideParser.ESC) | (1 << OverrideParser.WS) | (1 << OverrideParser.QUOTED_VALUE) | (1 << OverrideParser.INTERPOLATION))) != 0):
                        self.state = 36
                        self.value()




                pass
            elif token in [OverrideParser.PLUS]:
                self.state = 41
                self.match(OverrideParser.PLUS)
                self.state = 43
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==OverrideParser.PLUS:
                    self.state = 42
                    self.match(OverrideParser.PLUS)


                self.state = 45
                self.key()
                self.state = 46
                self.match(OverrideParser.EQUAL)
                self.state = 48
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << OverrideParser.COLON) | (1 << OverrideParser.BRACKET_OPEN) | (1 << OverrideParser.BRACE_OPEN) | (1 << OverrideParser.FLOAT) | (1 << OverrideParser.INT) | (1 << OverrideParser.BOOL) | (1 << OverrideParser.NULL) | (1 << OverrideParser.UNQUOTED_CHAR) | (1 << OverrideParser.ID) | (1 << OverrideParser.ESC) | (1 << OverrideParser.WS) | (1 << OverrideParser.QUOTED_VALUE) | (1 << OverrideParser.INTERPOLATION))) != 0):
                    self.state = 47
                    self.value()


                pass
            else:
                raise NoViableAltException(self)

            self.state = 52
            self.match(OverrideParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class KeyContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def packageOrGroup(self):
            return self.getTypedRuleContext(OverrideParser.PackageOrGroupContext,0)


        def AT(self):
            return self.getToken(OverrideParser.AT, 0)

        def package(self):
            return self.getTypedRuleContext(OverrideParser.PackageContext,0)


        def getRuleIndex(self):
            return OverrideParser.RULE_key

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterKey" ):
                listener.enterKey(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitKey" ):
                listener.exitKey(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitKey" ):
                return visitor.visitKey(self)
            else:
                return visitor.visitChildren(self)




    def key(self):

        localctx = OverrideParser.KeyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_key)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 54
            self.packageOrGroup()
            self.state = 57
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==OverrideParser.AT:
                self.state = 55
                self.match(OverrideParser.AT)
                self.state = 56
                self.package()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PackageOrGroupContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def package(self):
            return self.getTypedRuleContext(OverrideParser.PackageContext,0)


        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.ID)
            else:
                return self.getToken(OverrideParser.ID, i)

        def SLASH(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.SLASH)
            else:
                return self.getToken(OverrideParser.SLASH, i)

        def getRuleIndex(self):
            return OverrideParser.RULE_packageOrGroup

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPackageOrGroup" ):
                listener.enterPackageOrGroup(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPackageOrGroup" ):
                listener.exitPackageOrGroup(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPackageOrGroup" ):
                return visitor.visitPackageOrGroup(self)
            else:
                return visitor.visitChildren(self)




    def packageOrGroup(self):

        localctx = OverrideParser.PackageOrGroupContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_packageOrGroup)
        self._la = 0 # Token type
        try:
            self.state = 67
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 59
                self.package()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 60
                self.match(OverrideParser.ID)
                self.state = 63 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 61
                    self.match(OverrideParser.SLASH)
                    self.state = 62
                    self.match(OverrideParser.ID)
                    self.state = 65 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==OverrideParser.SLASH):
                        break

                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PackageContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(OverrideParser.ID, 0)

        def DOT_PATH(self):
            return self.getToken(OverrideParser.DOT_PATH, 0)

        def getRuleIndex(self):
            return OverrideParser.RULE_package

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPackage" ):
                listener.enterPackage(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPackage" ):
                listener.exitPackage(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPackage" ):
                return visitor.visitPackage(self)
            else:
                return visitor.visitChildren(self)




    def package(self):

        localctx = OverrideParser.PackageContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_package)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 72
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [OverrideParser.EOF, OverrideParser.EQUAL, OverrideParser.AT]:
                pass
            elif token in [OverrideParser.ID]:
                self.state = 70
                self.match(OverrideParser.ID)
                pass
            elif token in [OverrideParser.DOT_PATH]:
                self.state = 71
                self.match(OverrideParser.DOT_PATH)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def element(self):
            return self.getTypedRuleContext(OverrideParser.ElementContext,0)


        def simpleChoiceSweep(self):
            return self.getTypedRuleContext(OverrideParser.SimpleChoiceSweepContext,0)


        def getRuleIndex(self):
            return OverrideParser.RULE_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue" ):
                listener.enterValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue" ):
                listener.exitValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValue" ):
                return visitor.visitValue(self)
            else:
                return visitor.visitChildren(self)




    def value(self):

        localctx = OverrideParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_value)
        try:
            self.state = 76
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 74
                self.element()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 75
                self.simpleChoiceSweep()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def primitive(self):
            return self.getTypedRuleContext(OverrideParser.PrimitiveContext,0)


        def listContainer(self):
            return self.getTypedRuleContext(OverrideParser.ListContainerContext,0)


        def dictContainer(self):
            return self.getTypedRuleContext(OverrideParser.DictContainerContext,0)


        def function(self):
            return self.getTypedRuleContext(OverrideParser.FunctionContext,0)


        def getRuleIndex(self):
            return OverrideParser.RULE_element

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElement" ):
                listener.enterElement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElement" ):
                listener.exitElement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElement" ):
                return visitor.visitElement(self)
            else:
                return visitor.visitChildren(self)




    def element(self):

        localctx = OverrideParser.ElementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_element)
        try:
            self.state = 82
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 78
                self.primitive()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 79
                self.listContainer()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 80
                self.dictContainer()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 81
                self.function()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SimpleChoiceSweepContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OverrideParser.ElementContext)
            else:
                return self.getTypedRuleContext(OverrideParser.ElementContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.COMMA)
            else:
                return self.getToken(OverrideParser.COMMA, i)

        def getRuleIndex(self):
            return OverrideParser.RULE_simpleChoiceSweep

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSimpleChoiceSweep" ):
                listener.enterSimpleChoiceSweep(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSimpleChoiceSweep" ):
                listener.exitSimpleChoiceSweep(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSimpleChoiceSweep" ):
                return visitor.visitSimpleChoiceSweep(self)
            else:
                return visitor.visitChildren(self)




    def simpleChoiceSweep(self):

        localctx = OverrideParser.SimpleChoiceSweepContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_simpleChoiceSweep)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 84
            self.element()
            self.state = 87 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 85
                self.match(OverrideParser.COMMA)
                self.state = 86
                self.element()
                self.state = 89 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==OverrideParser.COMMA):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgNameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(OverrideParser.ID, 0)

        def EQUAL(self):
            return self.getToken(OverrideParser.EQUAL, 0)

        def getRuleIndex(self):
            return OverrideParser.RULE_argName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArgName" ):
                listener.enterArgName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArgName" ):
                listener.exitArgName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgName" ):
                return visitor.visitArgName(self)
            else:
                return visitor.visitChildren(self)




    def argName(self):

        localctx = OverrideParser.ArgNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_argName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 91
            self.match(OverrideParser.ID)
            self.state = 92
            self.match(OverrideParser.EQUAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(OverrideParser.ID, 0)

        def POPEN(self):
            return self.getToken(OverrideParser.POPEN, 0)

        def PCLOSE(self):
            return self.getToken(OverrideParser.PCLOSE, 0)

        def element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OverrideParser.ElementContext)
            else:
                return self.getTypedRuleContext(OverrideParser.ElementContext,i)


        def argName(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OverrideParser.ArgNameContext)
            else:
                return self.getTypedRuleContext(OverrideParser.ArgNameContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.COMMA)
            else:
                return self.getToken(OverrideParser.COMMA, i)

        def getRuleIndex(self):
            return OverrideParser.RULE_function

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunction" ):
                listener.enterFunction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunction" ):
                listener.exitFunction(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunction" ):
                return visitor.visitFunction(self)
            else:
                return visitor.visitChildren(self)




    def function(self):

        localctx = OverrideParser.FunctionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_function)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 94
            self.match(OverrideParser.ID)
            self.state = 95
            self.match(OverrideParser.POPEN)
            self.state = 110
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << OverrideParser.COLON) | (1 << OverrideParser.BRACKET_OPEN) | (1 << OverrideParser.BRACE_OPEN) | (1 << OverrideParser.FLOAT) | (1 << OverrideParser.INT) | (1 << OverrideParser.BOOL) | (1 << OverrideParser.NULL) | (1 << OverrideParser.UNQUOTED_CHAR) | (1 << OverrideParser.ID) | (1 << OverrideParser.ESC) | (1 << OverrideParser.WS) | (1 << OverrideParser.QUOTED_VALUE) | (1 << OverrideParser.INTERPOLATION))) != 0):
                self.state = 97
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
                if la_ == 1:
                    self.state = 96
                    self.argName()


                self.state = 99
                self.element()
                self.state = 107
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==OverrideParser.COMMA:
                    self.state = 100
                    self.match(OverrideParser.COMMA)
                    self.state = 102
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
                    if la_ == 1:
                        self.state = 101
                        self.argName()


                    self.state = 104
                    self.element()
                    self.state = 109
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 112
            self.match(OverrideParser.PCLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ListContainerContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BRACKET_OPEN(self):
            return self.getToken(OverrideParser.BRACKET_OPEN, 0)

        def BRACKET_CLOSE(self):
            return self.getToken(OverrideParser.BRACKET_CLOSE, 0)

        def element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OverrideParser.ElementContext)
            else:
                return self.getTypedRuleContext(OverrideParser.ElementContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.COMMA)
            else:
                return self.getToken(OverrideParser.COMMA, i)

        def getRuleIndex(self):
            return OverrideParser.RULE_listContainer

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterListContainer" ):
                listener.enterListContainer(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitListContainer" ):
                listener.exitListContainer(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitListContainer" ):
                return visitor.visitListContainer(self)
            else:
                return visitor.visitChildren(self)




    def listContainer(self):

        localctx = OverrideParser.ListContainerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_listContainer)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 114
            self.match(OverrideParser.BRACKET_OPEN)
            self.state = 123
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << OverrideParser.COLON) | (1 << OverrideParser.BRACKET_OPEN) | (1 << OverrideParser.BRACE_OPEN) | (1 << OverrideParser.FLOAT) | (1 << OverrideParser.INT) | (1 << OverrideParser.BOOL) | (1 << OverrideParser.NULL) | (1 << OverrideParser.UNQUOTED_CHAR) | (1 << OverrideParser.ID) | (1 << OverrideParser.ESC) | (1 << OverrideParser.WS) | (1 << OverrideParser.QUOTED_VALUE) | (1 << OverrideParser.INTERPOLATION))) != 0):
                self.state = 115
                self.element()
                self.state = 120
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==OverrideParser.COMMA:
                    self.state = 116
                    self.match(OverrideParser.COMMA)
                    self.state = 117
                    self.element()
                    self.state = 122
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 125
            self.match(OverrideParser.BRACKET_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DictContainerContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BRACE_OPEN(self):
            return self.getToken(OverrideParser.BRACE_OPEN, 0)

        def BRACE_CLOSE(self):
            return self.getToken(OverrideParser.BRACE_CLOSE, 0)

        def dictKeyValuePair(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OverrideParser.DictKeyValuePairContext)
            else:
                return self.getTypedRuleContext(OverrideParser.DictKeyValuePairContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.COMMA)
            else:
                return self.getToken(OverrideParser.COMMA, i)

        def getRuleIndex(self):
            return OverrideParser.RULE_dictContainer

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDictContainer" ):
                listener.enterDictContainer(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDictContainer" ):
                listener.exitDictContainer(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDictContainer" ):
                return visitor.visitDictContainer(self)
            else:
                return visitor.visitChildren(self)




    def dictContainer(self):

        localctx = OverrideParser.DictContainerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_dictContainer)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 127
            self.match(OverrideParser.BRACE_OPEN)
            self.state = 136
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << OverrideParser.FLOAT) | (1 << OverrideParser.INT) | (1 << OverrideParser.BOOL) | (1 << OverrideParser.NULL) | (1 << OverrideParser.UNQUOTED_CHAR) | (1 << OverrideParser.ID) | (1 << OverrideParser.ESC) | (1 << OverrideParser.WS) | (1 << OverrideParser.QUOTED_VALUE))) != 0):
                self.state = 128
                self.dictKeyValuePair()
                self.state = 133
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==OverrideParser.COMMA:
                    self.state = 129
                    self.match(OverrideParser.COMMA)
                    self.state = 130
                    self.dictKeyValuePair()
                    self.state = 135
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 138
            self.match(OverrideParser.BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DictKeyValuePairContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def dictKey(self):
            return self.getTypedRuleContext(OverrideParser.DictKeyContext,0)


        def COLON(self):
            return self.getToken(OverrideParser.COLON, 0)

        def element(self):
            return self.getTypedRuleContext(OverrideParser.ElementContext,0)


        def getRuleIndex(self):
            return OverrideParser.RULE_dictKeyValuePair

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDictKeyValuePair" ):
                listener.enterDictKeyValuePair(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDictKeyValuePair" ):
                listener.exitDictKeyValuePair(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDictKeyValuePair" ):
                return visitor.visitDictKeyValuePair(self)
            else:
                return visitor.visitChildren(self)




    def dictKeyValuePair(self):

        localctx = OverrideParser.DictKeyValuePairContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_dictKeyValuePair)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 140
            self.dictKey()
            self.state = 141
            self.match(OverrideParser.COLON)
            self.state = 142
            self.element()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimitiveContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUOTED_VALUE(self):
            return self.getToken(OverrideParser.QUOTED_VALUE, 0)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.ID)
            else:
                return self.getToken(OverrideParser.ID, i)

        def NULL(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.NULL)
            else:
                return self.getToken(OverrideParser.NULL, i)

        def INT(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.INT)
            else:
                return self.getToken(OverrideParser.INT, i)

        def FLOAT(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.FLOAT)
            else:
                return self.getToken(OverrideParser.FLOAT, i)

        def BOOL(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.BOOL)
            else:
                return self.getToken(OverrideParser.BOOL, i)

        def INTERPOLATION(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.INTERPOLATION)
            else:
                return self.getToken(OverrideParser.INTERPOLATION, i)

        def UNQUOTED_CHAR(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.UNQUOTED_CHAR)
            else:
                return self.getToken(OverrideParser.UNQUOTED_CHAR, i)

        def COLON(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.COLON)
            else:
                return self.getToken(OverrideParser.COLON, i)

        def ESC(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.ESC)
            else:
                return self.getToken(OverrideParser.ESC, i)

        def WS(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.WS)
            else:
                return self.getToken(OverrideParser.WS, i)

        def getRuleIndex(self):
            return OverrideParser.RULE_primitive

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimitive" ):
                listener.enterPrimitive(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimitive" ):
                listener.exitPrimitive(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimitive" ):
                return visitor.visitPrimitive(self)
            else:
                return visitor.visitChildren(self)




    def primitive(self):

        localctx = OverrideParser.PrimitiveContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_primitive)
        self._la = 0 # Token type
        try:
            self.state = 150
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [OverrideParser.QUOTED_VALUE]:
                self.enterOuterAlt(localctx, 1)
                self.state = 144
                self.match(OverrideParser.QUOTED_VALUE)
                pass
            elif token in [OverrideParser.COLON, OverrideParser.FLOAT, OverrideParser.INT, OverrideParser.BOOL, OverrideParser.NULL, OverrideParser.UNQUOTED_CHAR, OverrideParser.ID, OverrideParser.ESC, OverrideParser.WS, OverrideParser.INTERPOLATION]:
                self.enterOuterAlt(localctx, 2)
                self.state = 146 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 145
                    _la = self._input.LA(1)
                    if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << OverrideParser.COLON) | (1 << OverrideParser.FLOAT) | (1 << OverrideParser.INT) | (1 << OverrideParser.BOOL) | (1 << OverrideParser.NULL) | (1 << OverrideParser.UNQUOTED_CHAR) | (1 << OverrideParser.ID) | (1 << OverrideParser.ESC) | (1 << OverrideParser.WS) | (1 << OverrideParser.INTERPOLATION))) != 0)):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 148 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << OverrideParser.COLON) | (1 << OverrideParser.FLOAT) | (1 << OverrideParser.INT) | (1 << OverrideParser.BOOL) | (1 << OverrideParser.NULL) | (1 << OverrideParser.UNQUOTED_CHAR) | (1 << OverrideParser.ID) | (1 << OverrideParser.ESC) | (1 << OverrideParser.WS) | (1 << OverrideParser.INTERPOLATION))) != 0)):
                        break

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DictKeyContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUOTED_VALUE(self):
            return self.getToken(OverrideParser.QUOTED_VALUE, 0)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.ID)
            else:
                return self.getToken(OverrideParser.ID, i)

        def NULL(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.NULL)
            else:
                return self.getToken(OverrideParser.NULL, i)

        def INT(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.INT)
            else:
                return self.getToken(OverrideParser.INT, i)

        def FLOAT(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.FLOAT)
            else:
                return self.getToken(OverrideParser.FLOAT, i)

        def BOOL(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.BOOL)
            else:
                return self.getToken(OverrideParser.BOOL, i)

        def UNQUOTED_CHAR(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.UNQUOTED_CHAR)
            else:
                return self.getToken(OverrideParser.UNQUOTED_CHAR, i)

        def ESC(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.ESC)
            else:
                return self.getToken(OverrideParser.ESC, i)

        def WS(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.WS)
            else:
                return self.getToken(OverrideParser.WS, i)

        def getRuleIndex(self):
            return OverrideParser.RULE_dictKey

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDictKey" ):
                listener.enterDictKey(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDictKey" ):
                listener.exitDictKey(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDictKey" ):
                return visitor.visitDictKey(self)
            else:
                return visitor.visitChildren(self)




    def dictKey(self):

        localctx = OverrideParser.DictKeyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_dictKey)
        self._la = 0 # Token type
        try:
            self.state = 158
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [OverrideParser.QUOTED_VALUE]:
                self.enterOuterAlt(localctx, 1)
                self.state = 152
                self.match(OverrideParser.QUOTED_VALUE)
                pass
            elif token in [OverrideParser.FLOAT, OverrideParser.INT, OverrideParser.BOOL, OverrideParser.NULL, OverrideParser.UNQUOTED_CHAR, OverrideParser.ID, OverrideParser.ESC, OverrideParser.WS]:
                self.enterOuterAlt(localctx, 2)
                self.state = 154 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 153
                    _la = self._input.LA(1)
                    if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << OverrideParser.FLOAT) | (1 << OverrideParser.INT) | (1 << OverrideParser.BOOL) | (1 << OverrideParser.NULL) | (1 << OverrideParser.UNQUOTED_CHAR) | (1 << OverrideParser.ID) | (1 << OverrideParser.ESC) | (1 << OverrideParser.WS))) != 0)):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 156 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << OverrideParser.FLOAT) | (1 << OverrideParser.INT) | (1 << OverrideParser.BOOL) | (1 << OverrideParser.NULL) | (1 << OverrideParser.UNQUOTED_CHAR) | (1 << OverrideParser.ID) | (1 << OverrideParser.ESC) | (1 << OverrideParser.WS))) != 0)):
                        break

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





