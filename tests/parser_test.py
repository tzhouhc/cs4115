import unittest
from utils.lexer import TokenStream
from utils.token import Token, TokenType
from utils.parser import Parser, ASTNode, ASTMatchResult
from dataclasses import dataclass


@dataclass
class TestCase:
    input: TokenStream
    want_match: bool
    want_forward: int
    want:  str


class TestLexer(unittest.TestCase):
    def setUp(self):
        self.g = {
            "E": [
                ["RET_STAT"],
            ],
            "RET_STAT": [
                [
                    Token(TokenType.KEYWORD, "return"),
                    Token(TokenType.INTEGER, "")
                ],
                [
                    Token(TokenType.KEYWORD, "return"),
                    Token(TokenType.LPAREN, "("),
                    Token(TokenType.INTEGER, ""),
                    Token(TokenType.RPAREN, ")"),
                ],
                [
                    Token(TokenType.KEYWORD, "return"),
                    Token(TokenType.COLON, ":"),
                    "LIST_INT"
                ],
                [
                    Token(TokenType.KEYWORD, "return"),
                    Token(TokenType.COLON, ":"),
                    "OPT_ID"
                ],
            ],
            "LIST_INT": [
                [
                    Token(TokenType.INTEGER, ""),
                    "LIST_INT"
                ],
                [
                    "EPSILON"
                ]
            ],
            "OPT_ID": [
                [
                    Token(TokenType.ID, ""),
                ],
                [
                    "EPSILON",
                ]
            ]
        }

    def create_parser(self, tokens: TokenStream):
        return Parser(tokens, self.g)

    def run_test_case(self, name, test_case):
        with self.subTest(name=name):
            par = self.create_parser(test_case.input)
            got = par.parse(init_name="E")
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
            "E[RET_STAT[TokenType.KEYWORD(return), TokenType.INTEGER(42)]]"
        ))

    def test_basic_ret_stat_extra(self):
        self.run_test_case("basic ret_stat with extra tokens", TestCase(
            TokenStream([
                Token(TokenType.KEYWORD, "return"),
                Token(TokenType.INTEGER, "42"),
                Token(TokenType.KEYWORD, "if")
            ]),
            False, 0,
            "None"
        ))

    def test_basic_ret_stat_paren(self):
        self.run_test_case("basic ret_stat with parens", TestCase(
            TokenStream([
                Token(TokenType.KEYWORD, "return"),
                Token(TokenType.LPAREN, "("),
                Token(TokenType.INTEGER, "42"),
                Token(TokenType.RPAREN, ")"),
            ]),
            True, 4,
            "E[RET_STAT[TokenType.KEYWORD(return), TokenType.LPAREN((), "
            "TokenType.INTEGER(42), TokenType.RPAREN())]]"
        ))

    def test_ret_stat_list(self):
        self.run_test_case("basic ret_stat with list int", TestCase(
            TokenStream([
                Token(TokenType.KEYWORD, "return"),
                Token(TokenType.COLON, ":"),
                Token(TokenType.INTEGER, "42"),
                Token(TokenType.INTEGER, "42"),
                Token(TokenType.INTEGER, "42"),
            ]),
            True, 5,
            "E[RET_STAT[TokenType.KEYWORD(return), TokenType.COLON(:), "
            "LIST_INT[TokenType.INTEGER(42), "
            "LIST_INT[TokenType.INTEGER(42), "
            "LIST_INT[TokenType.INTEGER(42), EPSILON]]]]]"
        ))

    def test_ret_stat_list_empty(self):
        self.run_test_case("basic ret_stat with empty list int", TestCase(
            TokenStream([
                Token(TokenType.KEYWORD, "return"),
                Token(TokenType.COLON, ":"),
            ]),
            True, 2,
            "E[RET_STAT[TokenType.KEYWORD(return), TokenType.COLON(:), "
            "EPSILON]]"
        ))

    # Currently fails due to the syntax prioritizing matching the rule
    # above it, and not backtracking when that actually fails.
    def test_ret_stat_opt_id(self):
        self.run_test_case("basic ret_stat with optional id", TestCase(
            TokenStream([
                Token(TokenType.KEYWORD, "return"),
                Token(TokenType.COLON, ":"),
                Token(TokenType.ID, "var_1")
            ]),
            True, 3,
            "E[RET_STAT[TokenType.KEYWORD(return), TokenType.COLON(:), "
            "OPT_ID[TokenType.ID(var_1)]]]"
        ))


if __name__ == '__main__':
    unittest.main()
