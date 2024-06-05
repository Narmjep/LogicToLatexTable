from dataclasses import dataclass

@dataclass
class VariableNode:
    value: bool
    
    def __str__(self):
        return self.value

@dataclass
class ConjunctionNode:
    left: VariableNode
    right: VariableNode
    
    def __str__(self):
        return f"({self.left} & {self.right})"

@dataclass  
class DisjunctionNode:
    left: VariableNode
    right: VariableNode
    
    def __str__(self):
        return f"({self.left} | {self.right})"

@dataclass    
class ImplicationNode:
    left: VariableNode
    right: VariableNode
    
    def __str__(self):
        return f"({self.left} -> {self.right})"

@dataclass      
class BiconditionalNode:
    left: VariableNode
    right: VariableNode
    
    def __str__(self):
        return f"({self.left} <-> {self.right})"

@dataclass     
class ExclusiveOrNode:
    left: VariableNode
    right: VariableNode
    
    def __str__(self):
        return f"({self.left} + {self.right})"

@dataclass    
class EquivalenceNode:
    left: VariableNode
    right: VariableNode
    
    def __str__(self):
        return f"({self.left} = {self.right})"
    
@dataclass  
class NegationNode:
    value: VariableNode
    
    def __str__(self):
        return f"!{self.value}"