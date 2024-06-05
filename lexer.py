from tokens import *

class Lexer:
    def __init__(self, text, vars):
        # vars is a dictionary of variables and their values
        self.text = text
        self.text = text.replace(" ", "")
        for var in vars:
            self.text = self.text.replace(var, vars[var])
        self.pos = 0
        self.current_char = self.text[self.pos]
    def advance(self):
        self.pos += 1

        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def get_var(self):
        result = ""
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        return Token(TokenType.VARIABLE, result)
    
    def get_operator(self):
        result = ""
        while self.current_char is not None and self.current_char in operator_chars:
            result += self.current_char
            self.advance()
        return Token(TokenType.OPERATOR, result)
    
    def get_tokens(self):
        tokens = []
        while self.current_char is not None:
            #Variable
            if self.current_char in ('1', '0'):
                token = Token(TokenType.VARIABLE, self.current_char)
                self.advance()
                tokens.append(token)
            #Operator
            if self.current_char in operator_chars:
                tokens.append(self.get_operator())
            #Parentheses
            if self.current_char == "(":
                token = Token(TokenType.LPAREN, self.current_char)
                self.advance()
                tokens.append(token)
            if self.current_char == ")":
                token = Token(TokenType.RPAREN, self.current_char)
                self.advance()
                tokens.append(token)
            #Negation
            if self.current_char == "!":
                token = Token(TokenType.NEGATION, self.current_char)
                self.advance()
                tokens.append(token)

            if self.current_char is None:
                break
            
        return tokens
            


