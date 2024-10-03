from .grammar import TokenType


class Lexer:

    def __init__(self, input: str) -> None:
        self.input = input
        self.pos = 0
        self.max = len(input)

    def step(self) -> None:
        self.pos += 1
        if self.pos >= self.max:
            raise IndexError(f"Reached end of input at pos {self.max}")

    def current(self) -> str:
        return self.input[self.pos]

    def lookahead(self) -> str:
        if self.pos < self.max - 1:
            return self.input[self.pos + 1]
        return ""

    def lex(self) -> list[tuple[TokenType, str]]:
        return []
