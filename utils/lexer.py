import argparse
import logging
from typing import Callable, Optional
from utils.token import Token, TokenType
from utils.dfa import EOL, NoPaths, SimpleAutomata, UnknownChar

logger = logging.getLogger(__name__)


class TokenStream:
    def __init__(self, init: Optional[list[Token]] = None) -> None:
        """
        Initialize a TokenStream object.

        Parameters:
        init (Optional[list[Token]]): Optional initial list of tokens to
        initialize the TokenStream with.

        Returns:
        None
        """
        self.tokens = []
        if init:
            self.tokens: list[Token] = init

    def __getitem__(self, i: int) -> Token:
        return self.tokens[i]

    def __len__(self) -> int:
        return len(self.tokens)

    def __str__(self) -> str:
        """
        Return a string representation of the TokenStream.

        Returns:
        str: String representation of the TokenStream.
        """
        res = ""
        for token in self.tokens:
            res += f"\t{str(token)}\n"
        return res

    def __repr__(self) -> str:
        """
        Return a string representation of the TokenStream for debugging
        purposes.

        Returns:
        str: String representation of the TokenStream.
        """
        res = "TokenStream([\n"
        for token in self.tokens:
            res += f"\t{repr(token)},\n"
        res += "])"
        return res

    def __eq__(self, o) -> bool:
        """
        Check if two TokenStream objects are equal.

        Parameters:
        o: Another TokenStream object to compare with.

        Returns:
        bool: True if the two TokenStream objects are equal, False otherwise.
        """
        if len(self.tokens) != len(o.tokens):
            return False
        return all(
            [
                self.tokens[i] == o.tokens[i]
                for i in range(0, len(self.tokens))
            ]
        )

    def append(self, t: Optional[Token]) -> None:
        """
        Append a token to the TokenStream.

        Parameters:
        t (Optional[Token]): Token to append to the TokenStream.

        Returns:
        None
        """
        if t:
            self.tokens += [t]

    def filter(self, f: Callable[[Token], bool]) -> None:
        """
        Filter the tokens in the TokenStream based on a given filter function.

        Parameters:
        f (Callable[[Token], bool]): Filter function that takes a Token as
        input and returns a boolean.

        Returns:
        None
        """
        self.tokens = [t for t in self.tokens if f(t)]


class LexerOptions(argparse.Namespace):

    def __init__(self):
        """
        Initialize a LexerOptions object.

        Returns:
        None
        """
        self.whitespace = True


class Lexer:
    """
    A class for lexing input strings using a deterministic finite automaton
    (DFA).

    Args:
        input (str): The input string to be lexed.
        dfa (SimpleAutomata): The DFA used for lexing.
        options (LexerOptions, optional): Options for customizing the lexer
        behavior. Defaults to None.

    Attributes:
        input (str): The input string to be lexed.
        pos (int): The current position in the input string.
        max (int): The maximum length of the input string.
        dfa (SimpleAutomata): The DFA used for lexing.
        options (LexerOptions): Options for customizing the lexer behavior.

    Methods:
        step(): Move to the next character in the input string.
        current() -> str: Get the current character in the input string.
        lookahead() -> str: Get the next character in the input string.
        done() -> bool: Check if the lexer has reached the end of the input
        string.
        lex() -> TokenStream: Lex the input string and return a stream of
        tokens.

    Raises:
        UnknownChar: If an unknown character is encountered during lexing.
        EOL: If the end of the input string is reached.
        NoPaths: If there are no valid transitions from the current state in
        the DFA.

    Returns:
        TokenStream: A stream of tokens generated by lexing the input string.
    """

    def __init__(self, input: str, dfa: SimpleAutomata,
                 options: Optional[argparse.Namespace] = None) -> None:
        self.input = input
        self.pos = 0
        self.max = len(input)
        self.dfa = dfa
        self.options = LexerOptions()
        if options:
            self.options = options

    def step(self) -> None:
        """Move to the next character in the input string."""
        self.pos += 1

    def current(self) -> str:
        """Get the current character in the input string."""
        return self.input[self.pos]

    def lookahead(self) -> str:
        """Get the next character in the input string."""
        if self.pos < self.max - 1:
            return self.input[self.pos + 1]
        return ""

    def done(self) -> bool:
        """Check if the lexer has reached the end of the input string."""
        return self.pos > self.max

    def lex(self) -> TokenStream:
        """
        Lex the input string and return a stream of tokens.

        Returns:
            TokenStream: A stream of tokens generated by lexing the input
            string.
        """
        res = TokenStream()
        while not self.done():
            if self.pos == self.max:
                c = ''
            else:
                c = self.current()
            logger.debug(f"Currently at {self.pos}")

            try:
                logger.debug(f"Received char '{c}'")
                self.dfa.step(c)
            except UnknownChar:
                logger.debug(f"Unknown character '{c}'")
                res.append(self.dfa.do_return())
                # should step to move past
            except EOL:
                logger.debug("Reached EOL")
                res.append(self.dfa.do_return())
                # nothing more to do
                break
            except NoPaths:
                logger.debug(f"Unable to step from current state {
                             self.dfa.current} with '{c}'")
                res.append(self.dfa.do_return())
                # should not step so that we can start with 'start'
                continue
            self.step()

        if not self.options.whitespace:
            res.filter(lambda t: t.type != TokenType.WHITE_SPACE)
        return res
