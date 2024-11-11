from enum import Enum, auto


class TokenType(Enum):
    EOL = 0  # special case for e.g. empty string
    WHITE_SPACE = auto()  # \s
    LPAREN = auto()  # (
    RPAREN = auto()  # )
    LBRACKET = auto()  # [
    RBRACKET = auto()  # ]
    LCURLY = auto()  # {
    RCURLY = auto()  # }
    COLON = auto()  # :
    SEMICOLON = auto()  # ;
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
    STRING = auto()

    ERROR = auto()
    EOF = auto()


# KEYWORD and OP now also must match strictly since the syntax has provided
# the full matching guidelines
VARIABLE_TOKENS = [
    TokenType.INTEGER, TokenType.FLOAT,
    TokenType.STRING, TokenType.WHITE_SPACE, TokenType.ID
]


class Token:
    def __init__(self, t: TokenType, s: str = "") -> None:
        """
        Initialize a Token object with the given TokenType and optional string.

        Parameters:
        t (TokenType): The type of the token.
        s (str): The string associated with the token. Default is an empty
        string.

        Returns:
        None
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

    def __repr__(self) -> str:
        """
        Return a string representation of the Token object for debugging.

        Returns:
        str: A string representation of the Token object.
        """
        return f"Token({self.type}, '{self.string}')"

    def __eq__(self, o) -> bool:
        """
        Check if two Token objects are equal.

        Parameters:
        o (Token): The other Token object to compare.

        Returns:
        bool: True if the two Token objects are equal, False otherwise.
        """
        return isinstance(o, Token) and \
            self.type == o.type and self.string == o.string

    def __hash__(self) -> int:
        # Hash tuple of the enum value and string
        return hash((self.type, self.string))

    def append(self, c: str) -> None:
        """
        Append a character to the string associated with the Token object.

        Parameters:
        c (str): The character to append to the string.

        Returns:
        None
        """
        self.string += c
