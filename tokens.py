from enum import Enum
from dataclasses import dataclass

operators = {'&', '|', '->', '<->', '+', '=', '~'}

operator_chars = []

for op in operators:
    for char in op:
        if char not in operator_chars:
            operator_chars.append(char)

class TokenType(Enum):
    VARIABLE = 1
    OPERATOR = 2
    LPAREN = 3
    RPAREN = 4
    NEGATION = 5

@dataclass
class Token:
    type: TokenType
    value: str

    def __str__(self):
        return f"Token({self.type}, {self.value})"
    
    def __repr__(self):
        return self.__str__()
    

