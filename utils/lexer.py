from .token import Token
from .dfa import SimpleAutomata


class TokenStream:
    def __init__(self) -> None:
        """
        Initialize a TokenStream object with an empty list of tokens.
        """
        self.tokens: list[Token] = []

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

    def append(self, t: Token) -> None:
        """
        Appends a token to the TokenStream.

        Args:
        t: A Token object to append.
        """
        self.tokens += [t]


class Lexer:

    def __init__(self, input: str, dfa: SimpleAutomata) -> None:
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

    def step(self) -> None:
        """
        Increment the position in the input string by one.

        Raises:
        IndexError: If the position exceeds the maximum length of the input
        string.
        """
        self.pos += 1
        if self.pos >= self.max:
            raise IndexError(f"Reached end of input at pos {self.max}")

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
            print(f"Received char '{c}")
            try:
                self.dfa.step(c)
            except ValueError as e:
                if self.dfa.can_return():
                    res.append(self.dfa.do_return())
                else:
                    raise e
                self.dfa.reset()
                continue
            try:
                self.step()
            except IndexError:
                if self.dfa.can_return():
                    res.append(self.dfa.do_return())
                return res

        return TokenStream()
