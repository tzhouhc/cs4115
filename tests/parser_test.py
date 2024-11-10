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
            self.assertEqual(test_case.want, str(got),
                             f"Testcase '{name}' error: want:\n"
                             f"{test_case.want}, got:\n{str(got)}\n")

    def test_empty_string(self):
        self.run_test_case("basic ret_stat", TestCase(
            TokenStream([
                Token(TokenType.KEYWORD, "return"),
                Token(TokenType.INTEGER, "42")
            ]),
            True, 2,
            "E[RET_STAT[TokenType.KEYWORD(return), TokenType.INTEGER(42)]]"
        ))


if __name__ == '__main__':
    unittest.main()
