import unittest
from utils.lexer import TokenStream
from utils.token import Token, TokenType
from utils.parser import Parser, SYNTAX_MAP
from dataclasses import dataclass


@dataclass
class TestCase:
    input: TokenStream
    want_match: bool
    want_forward: int
    want:  str


class TestLuaParser(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.g = SYNTAX_MAP

    def create_parser(self, tokens: TokenStream):
        return Parser(tokens, self.g)

    def run_test_case(self, name, test_case):
        with self.subTest(name=name):
            par = self.create_parser(test_case.input)
            got = par.parse()
            self.assertEqual(test_case.want_match, got.match)
            self.assertEqual(test_case.want_forward, got.forward)
            self.assertEqual(test_case.want, str(got))

    def test_basic_ret_stat(self):
        self.run_test_case("basic ret_stat", TestCase(
            TokenStream([
                Token(TokenType.KEYWORD, "return"),
                Token(TokenType.INTEGER, "42")
            ]),
            True, 2,
            "CHUNK[BLOCK[OPT_RETSTAT[RETSTAT[TokenType.KEYWORD(return), "
            "OPT_EXPLIST[EXPLIST[EXP[SIMPLE_EXP[TokenType.INTEGER(42)]]]]]]]]"
        ))

    def test_basic_stat(self):
        self.run_test_case("basic statement", TestCase(
            TokenStream([
                Token(TokenType.ID, "a"),
                Token(TokenType.OP, "="),
                Token(TokenType.INTEGER, "4"),
            ]),
            True, 3,
            "CHUNK[BLOCK[LIST_STAT[STAT[VARLIST[VAR[PRIMARYEXP"
            "[TokenType.ID(a)]]], "
            "TokenType.OP(=), "
            "EXPLIST[EXP[SIMPLE_EXP[TokenType.INTEGER(4)]]]]]]]"
        ))

    def test_basic_stats(self):
        self.run_test_case("basic statement list", TestCase(
            TokenStream([
                Token(TokenType.ID, "a"),
                Token(TokenType.OP, "="),
                Token(TokenType.INTEGER, "4"),
                Token(TokenType.ID, "b"),
                Token(TokenType.OP, "="),
                Token(TokenType.INTEGER, "5"),
            ]),
            True, 6,
            "CHUNK[BLOCK[LIST_STAT[STAT[VARLIST[VAR[PRIMARYEXP"
            "[TokenType.ID(a)]]], "
            "TokenType.OP(=), "
            "EXPLIST[EXP[SIMPLE_EXP[TokenType.INTEGER(4)]]]], "
            "LIST_STAT[STAT[VARLIST[VAR[PRIMARYEXP[TokenType.ID(b)]]], "
            "TokenType.OP(=), "
            "EXPLIST[EXP[SIMPLE_EXP[TokenType.INTEGER(5)]]]]]]]]"
        ))

    def test_basic_stats_w_ret_stat(self):
        self.run_test_case("basic statement list with a return", TestCase(
            TokenStream([
                Token(TokenType.ID, "a"),
                Token(TokenType.OP, "="),
                Token(TokenType.INTEGER, "4"),
                Token(TokenType.ID, "b"),
                Token(TokenType.OP, "="),
                Token(TokenType.INTEGER, "5"),
                Token(TokenType.KEYWORD, "return"),
                Token(TokenType.LPAREN, "("),
                Token(TokenType.ID, "a"),
                Token(TokenType.OP, "+"),
                Token(TokenType.ID, "b"),
                Token(TokenType.RPAREN, ")"),
            ]),
            True, 12,
            "CHUNK["
            "BLOCK[LIST_STAT[STAT[VARLIST[VAR[PRIMARYEXP[TokenType.ID(a)]]], "
            "TokenType.OP(=), "
            "EXPLIST[EXP[SIMPLE_EXP[TokenType.INTEGER(4)]]]], "
            "LIST_STAT[STAT[VARLIST[VAR[PRIMARYEXP[TokenType.ID(b)]]], "
            "TokenType.OP(=), "
            "EXPLIST[EXP[SIMPLE_EXP[TokenType.INTEGER(5)]]]]]], "
            "OPT_RETSTAT[RETSTAT[TokenType.KEYWORD(return), "
            "OPT_EXPLIST[EXPLIST[EXP[SIMPLE_EXP[PREFIXEXP[PRIMARYEXP"
            "[TokenType.LPAREN((), "
            "EXP[SIMPLE_EXP[PREFIXEXP[PRIMARYEXP[TokenType.ID(a)], "
            "LIST_SUFFIX[SUFFIX[VARSUFFIX[TokenType.OP(+), "
            "TokenType.ID(b)]]]]]], TokenType.RPAREN())]]]]]]]]]]"
        ))


if __name__ == '__main__':
    unittest.main()
