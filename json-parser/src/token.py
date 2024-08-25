
from enum import Enum

class TokenTypes(Enum):
    LEFT_BRACE = "left_brace" # {
    RIGTH_BRACE = "right_brace" # }
    STRING = "string" # a string
    COLON = ":" # colong token type
    EOF = "eof" # mark end of file
    COMMA = "comma" # comma `,`

class Token:
    def __init__(self, literal: str, type: TokenTypes) -> None:
        self.literal = literal
        self.type = type

    def __repr__(self) -> str:
        return f"Token[literal: '{self.literal}', type: {self.type.name}]"
