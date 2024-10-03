from enum import Enum, auto


class TokenType(Enum):
    WHITE_SPACE = 0
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    ID = auto()
    EQUALS = auto()
    INTEGER = auto()
    FLOAT = auto()
