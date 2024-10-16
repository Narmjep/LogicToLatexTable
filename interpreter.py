from nodes import *

class Interpreter:
    def __init__(self):
        pass

    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name)
        return visitor(node, node.negated if hasattr(node, 'negated') else False)
    
    def visit_VariableNode(self, node, negated=False):
        return node.value == '1'
    
    def visit_ConjunctionNode(self, node, negated=False):
        result = self.visit(node.left) and self.visit(node.right)
        return not result if negated else result

    
    def visit_DisjunctionNode(self, node, negated=False):
        result = self.visit(node.left) or self.visit(node.right)
        return not result if negated else result
        
    
    def visit_ImplicationNode(self, node, negated=False):
        result = not self.visit(node.left) or self.visit(node.right)
        return not result if negated else result
    
    def visit_ExclusiveOrNode(self, node, negated=False):
        result = self.visit(node.left) != self.visit(node.right)
        return not result if negated else result
    
    def visit_EquivalenceNode(self, node, negated=False):
        result = self.visit(node.left) == self.visit(node.right)
        return not result if negated else result
    
    def visit_NegationNode(self, node, negated=False):
        return not self.visit(node.value)
    
