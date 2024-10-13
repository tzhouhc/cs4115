import unittest
from utils import lexer, grammar, dfa
from utils.token import Token, TokenType
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
                             f"{test_case.want}, got:\n{repr(got)}\n")

    def test_empty_string(self):
        self.run_test_case("empty_string", TestCase("", lexer.TokenStream()))

    def test_hello_world(self):
        self.run_test_case("hello world",
                           TestCase("hello world", lexer.TokenStream([
                               Token(TokenType.ID, "hello"),
                               Token(TokenType.WHITE_SPACE, " "),
                               Token(TokenType.ID, "world"),
                           ])))

    def test_ambiguity(self):
        self.run_test_case("ambiguity",
                           TestCase("for fora fo fun func", lexer.TokenStream([
                               Token(TokenType.KEYWORD, "for"),
                               Token(TokenType.WHITE_SPACE, " "),
                               Token(TokenType.ID, "fora"),
                               Token(TokenType.WHITE_SPACE, " "),
                               Token(TokenType.ID, "fo"),
                               Token(TokenType.WHITE_SPACE, " "),
                               Token(TokenType.ID, "fun"),
                               Token(TokenType.WHITE_SPACE, " "),
                               Token(TokenType.KEYWORD, "func"),
                           ])))

    def test_hello_world_str(self):
        self.run_test_case("hello world string",
                           TestCase("\"hello world\"", lexer.TokenStream([
                               Token(TokenType.STRING, "\"hello world\""),
                           ])))

    def test_str_with_escape(self):
        self.run_test_case("str with escape",
                           TestCase("\"some\\\" stuff\"", lexer.TokenStream([
                               Token(TokenType.STRING, "\"some\\\" stuff\""),
                           ])))

    def test_bad_tokens(self):
        self.run_test_case("bad_tokens",
                           TestCase(". . * * ", lexer.TokenStream([
                               Token(TokenType.ERROR, "."),
                               Token(TokenType.WHITE_SPACE, " "),
                               Token(TokenType.ERROR, "."),
                               Token(TokenType.WHITE_SPACE, " "),
                               Token(TokenType.ERROR, "*"),
                               Token(TokenType.WHITE_SPACE, " "),
                               Token(TokenType.ERROR, "*"),
                               Token(TokenType.WHITE_SPACE, " "),
                           ])))

    def test_bad_tokens_2(self):
        self.run_test_case("bad tokens 2",
                           TestCase(". . * *", lexer.TokenStream([
                               Token(TokenType.ERROR, "."),
                               Token(TokenType.WHITE_SPACE, " "),
                               Token(TokenType.ERROR, "."),
                               Token(TokenType.WHITE_SPACE, " "),
                               Token(TokenType.ERROR, "*"),
                               Token(TokenType.WHITE_SPACE, " "),
                               Token(TokenType.ERROR, "*"),
                           ])))

    def test_space(self):
        self.run_test_case("space", TestCase(" ", lexer.TokenStream(
            [Token(TokenType.WHITE_SPACE, ' ')])))

    def test_parens(self):
        self.run_test_case("parens", TestCase("(())", lexer.TokenStream([
            Token(TokenType.LPAREN, "("),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.RPAREN, ")"),
        ])))

    def test_function_decl(self):
        self.run_test_case(
            "function decl",
            TestCase("function(n) n = n + 1 end", lexer.TokenStream([
                Token(TokenType.ID, 'function'),
                Token(TokenType.LPAREN, '('),
                Token(TokenType.ID, 'n'),
                Token(TokenType.RPAREN, ')'),
                Token(TokenType.WHITE_SPACE, ' '),
                Token(TokenType.ID, 'n'),
                Token(TokenType.WHITE_SPACE, ' '),
                Token(TokenType.OP, '='),
                Token(TokenType.WHITE_SPACE, ' '),
                Token(TokenType.ID, 'n'),
                Token(TokenType.WHITE_SPACE, ' '),
                Token(TokenType.OP, '+'),
                Token(TokenType.WHITE_SPACE, ' '),
                Token(TokenType.INTEGER, '1'),
                Token(TokenType.WHITE_SPACE, ' '),
                Token(TokenType.KEYWORD, 'end'),
            ])))

    def test_various_types(self):
        self.run_test_case(
            "various types",
            TestCase("echo 13 1 + 2 - 7 else got while whi ile endif",
                     lexer.TokenStream([
                         Token(TokenType.ID, 'echo'),
                         Token(TokenType.WHITE_SPACE, ' '),
                         Token(TokenType.INTEGER, '13'),
                         Token(TokenType.WHITE_SPACE, ' '),
                         Token(TokenType.INTEGER, '1'),
                         Token(TokenType.WHITE_SPACE, ' '),
                         Token(TokenType.OP, '+'),
                         Token(TokenType.WHITE_SPACE, ' '),
                         Token(TokenType.INTEGER, '2'),
                         Token(TokenType.WHITE_SPACE, ' '),
                         Token(TokenType.OP, '-'),
                         Token(TokenType.WHITE_SPACE, ' '),
                         Token(TokenType.INTEGER, '7'),
                         Token(TokenType.WHITE_SPACE, ' '),
                         Token(TokenType.KEYWORD, 'else'),
                         Token(TokenType.WHITE_SPACE, ' '),
                         Token(TokenType.ID, 'got'),
                         Token(TokenType.WHITE_SPACE, ' '),
                         Token(TokenType.KEYWORD, 'while'),
                         Token(TokenType.WHITE_SPACE, ' '),
                         Token(TokenType.ID, 'whi'),
                         Token(TokenType.WHITE_SPACE, ' '),
                         Token(TokenType.ID, 'ile'),
                         Token(TokenType.WHITE_SPACE, ' '),
                         Token(TokenType.ID, 'endif'),
                     ])))

    def test_parens_with_error(self):
        self.run_test_case(
            "parens with error", TestCase("((.))", lexer.TokenStream([
                Token(TokenType.LPAREN, "("),
                Token(TokenType.LPAREN, "("),
                Token(TokenType.ERROR, "."),
                Token(TokenType.RPAREN, ")"),
                Token(TokenType.RPAREN, ")"),
            ])))

        if __name__ == '__main__':
            unittest.main()
