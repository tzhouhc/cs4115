import argparse
import logging
from typing import Callable, Optional
from utils.token import Token, TokenType
from utils.dfa import SimpleAutomata

logger = logging.getLogger(__name__)


class TokenStream:
    def __init__(self, init: Optional[list[Token]] = None) -> None:
        """
        Initialize a TokenStream object with an empty list of tokens.
        """
        self.tokens = []
        if init:
            self.tokens: list[Token] = init

    def __str__(self) -> str:
        """
        Return a string representation of the TokenStream object.

        Returns:
        str: A string representation of the TokenStream object.
        """
        res = ""
        for token in self.tokens:
            res += f"\t{str(token)}\n"
        return res

    def __repr__(self) -> str:
        """
        Return a string recreation of the TokenStream object.

        Returns:
        str: A string recreation of the TokenStream object.
        """
        res = "TokenStream([\n"
        for token in self.tokens:
            res += f"\t{repr(token)},\n"
        res += "])"
        return res

    def __eq__(self, o) -> bool:
        return all(
            [
                self.tokens[i] == o.tokens[i]
                for i in range(0, len(self.tokens))
            ]
        )

    def append(self, t: Token) -> None:
        """
        Appends a token to the TokenStream.

        Args:
        t: A Token object to append.
        """
        self.tokens += [t]

    def filter(self, f: Callable[[Token], bool]) -> None:
        self.tokens = [t for t in self.tokens if f(t)]


class LexerOptions(argparse.Namespace):

    def __init__(self):
        self.whitespace = True


class Lexer:

    def __init__(self, input: str, dfa: SimpleAutomata,
                 options: Optional[LexerOptions] = None) -> None:
        """
        Initialize a Lexer object with the input string, position, and maximum
        length.

        Parameters:
        input (str): The input string to be lexed.
        """
        self.input = input
        self.pos = 0
        self.max = len(input)
        self.dfa = dfa
        self.options = LexerOptions()
        if options:
            self.options = options

    def step(self) -> None:
        """
        Increment the position in the input string by one.

        Raises:
        IndexError: If the position exceeds the maximum length of the input
        string.
        """
        self.pos += 1

    def current(self) -> str:
        """
        Return the current character at the current position in the input
        string.

        Returns:
        str: The current character at the current position.
        """
        return self.input[self.pos]

    def lookahead(self) -> str:
        """
        Return the next character in the input string.

        Returns:
        str: The next character in the input string, or an empty string if at
        the end.
        """
        if self.pos < self.max - 1:
            return self.input[self.pos + 1]
        return ""

    def done(self) -> bool:
        return self.pos == self.max

    def lex(self) -> TokenStream:
        """
        Lex the input string and return a TokenStream object.

        Returns:
        TokenStream: A TokenStream object containing the tokens generated from
        the input string.
        """
        res = TokenStream()
        while not self.done():
            c = self.current()
            logger.debug(f"Received char '{c}'")
            try:
                self.dfa.step(c)
            except ValueError as e:
                if self.dfa.can_return():
                    res.append(self.dfa.do_return())
                    continue
                else:
                    logger.debug(e)
                    res.append(self.dfa.do_error())
            self.step()
        # Final token gets stuck in the pipeline, oops
        if self.dfa.can_return():
            res.append(self.dfa.do_return())

        if not self.options.whitespace:
            res.filter(lambda t: t.type != TokenType.WHITE_SPACE)
        return res
