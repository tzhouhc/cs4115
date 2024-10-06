from enum import Enum, auto


class TokenType(Enum):
    WHITE_SPACE = 0  # \s
    LPAREN = auto()  # (
    RPAREN = auto()  # )
    LBRACKET = auto()  # [
    RBRACKET = auto()  # ]
    KEYWORD = auto()
    # The following are reserved as keywords:
    # and       break     do        else      elseif    end
    # false     for       function  goto      if        in
    # local     nil       not       or        repeat    return
    # then      true      until     while
    ID = auto()
    # Names (also called identifiers) in Lua can be any string of Latin
    # letters, Arabic-Indic digits, and underscores, not beginning with a digit
    # and not being a reserved word. Identifiers are used to name variables,
    # table fields, and labels.
    OP = auto()
    COMMA = auto()
    INTEGER = auto()
    FLOAT = auto()


class Token:
    def __init__(self, t: TokenType, s: str = "") -> None:
        """
        Initialize a Token object with a TokenType and a string value.

        Parameters:
        t (TokenType): The type of the token.
        s (str): The string value of the token.
        """
        self.type = t
        self.string = s

    def __str__(self) -> str:
        """
        Return a string representation of the Token object.

        Returns:
        str: A string representation of the Token object.
        """
        return f"<{self.type}, '{self.string}'>"

    def append(self, c) -> None:
        self.string += c
