import unittest
from utils import lexer, grammar, dfa, token
from dataclasses import dataclass


@dataclass
class TestCase:
    input: str
    want: lexer.TokenStream


class TestLexer(unittest.TestCase):
    def setUp(self):
        self.g = grammar.STATE_TABLE

    def create_lexer(self, input_str):
        return lexer.Lexer(input_str, dfa.SimpleAutomata(self.g))

    def run_test_case(self, name, test_case):
        with self.subTest(name=name):
            lex = self.create_lexer(test_case.input)
            got = lex.lex()
            self.assertEqual(test_case.want, got,
                             f"Testcase '{name}' error: want:\n"
                             f"{test_case.want}, got:\n{got}\n")

    def test_empty_string(self):
        self.run_test_case("empty_string", TestCase("", lexer.TokenStream()))

    def test_hello_world(self):
        self.run_test_case("hello world",
                           TestCase("hello world", lexer.TokenStream([
                               token.Token(token.TokenType.ID, "hello"),
                               token.Token(token.TokenType.WHITE_SPACE, " "),
                               token.Token(token.TokenType.ID, "world"),
                           ])))

    def test_space(self):
        self.run_test_case("space", TestCase(" ", lexer.TokenStream(
            [token.Token(token.TokenType.WHITE_SPACE, ' ')])))

    def test_parens(self):
        self.run_test_case("parens", TestCase("(())", lexer.TokenStream([
            token.Token(token.TokenType.LPAREN, "("),
            token.Token(token.TokenType.LPAREN, "("),
            token.Token(token.TokenType.RPAREN, ")"),
            token.Token(token.TokenType.RPAREN, ")"),
        ])))


if __name__ == '__main__':
    unittest.main()
