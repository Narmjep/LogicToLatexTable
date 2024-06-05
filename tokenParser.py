from tokens import *
from nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def error(self):
        raise Exception("Error: Invalid syntax")
    
    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def parse(self):
        if self.current_token is None:
            return None
        
        result = self.expr()

        if self.current_token is not None:
            self.error()

        return result
    
    def expr(self):
        result = self.term()
        
        while self.current_token is not None and self.current_token.type == TokenType.OPERATOR:
            # operations that come later in the order of operations
            if self.current_token.value == "->":
                self.advance()
                result = ImplicationNode(result, self.term())
            elif self.current_token.value == "<->":
                self.advance()
                result = BiconditionalNode(result, self.term())
            elif self.current_token.value == "+":
                self.advance()
                result = ExclusiveOrNode(result, self.term())
            elif self.current_token.value == "=":
                self.advance()
                result = EquivalenceNode(result, self.term())
            elif self.current_token.value == "|":
                self.advance()
                result = DisjunctionNode(result, self.term())
            else :
                raise Exception("Error: Invalid syntax "+self.current_token.value)

        return result
    
    def term(self):
        result = self.factor()

        while self.current_token is not None and self.current_token.value == "&":
            # operations that come first in the order of operations
            if self.current_token.type == TokenType.OPERATOR and self.current_token.value == "&":
                self.advance()
                result = ConjunctionNode(result, self.factor())

        return result
    
    def factor(self):

        token = self.current_token

        if token.type == TokenType.LPAREN:
            self.advance()
            result = self.expr()
            if self.current_token.type != TokenType.RPAREN:
                self.error()
            self.advance()
            return result
        
        elif token.type == TokenType.VARIABLE:
            self.advance()
            return VariableNode(token.value)
    
        elif token.type == TokenType.NEGATION:
            self.advance()
            return NegationNode(self.factor())