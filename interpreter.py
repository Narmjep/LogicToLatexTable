from nodes import *

class Interpreter:
    def __init__(self):
        pass

    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name)
        return visitor(node)
    
    def visit_VariableNode(self, node):
        return node.value == '1'
    
    def visit_ConjunctionNode(self, node):
        return self.visit(node.left) and self.visit(node.right)
    
    def visit_DisjunctionNode(self, node):
        return self.visit(node.left) or self.visit(node.right)
    
    def visit_ImplicationNode(self, node):
        return not self.visit(node.left) or self.visit(node.right)
    
    def visit_BiconditionalNode(self, node):
        return self.visit(node.left) == self.visit(node.right)
    
    def visit_ExclusiveOrNode(self, node):
        return self.visit(node.left) != self.visit(node.right)
    
    def visit_EquivalenceNode(self, node):
        return self.visit(node.left) == self.visit(node.right)
    
    def visit_NegationNode(self, node):
        return not self.visit(node.value)
    
