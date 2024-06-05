from lexer import *
from tokenParser import *
from interpreter import *


def test(expr, expected):
    if expr == expected:
        print("PASSED")
    else:
        print("FAILED")
        print("Expected: ", expected)
        print("Got: ", expr)

def get_vars(expr):
    vars = {}
    for i in range(len(expr)):
        if expr[i].isalpha():
            vars[expr[i]] = '1'
    return vars

def test_expr(expr, expected):
    vars = get_vars(expr)
    lexer = Lexer(expr, vars)
    tokens = lexer.get_tokens()
    tree = Parser(tokens).parse()
    res = Interpreter().visit(tree)
    test(res, expected)

test_expr("1  ", True)
test_expr("0", False)
test_expr("1&1", True)
test_expr("1&0", False)
test_expr("0&1", False)
test_expr("1 | 1", True)
test_expr("1 | 0", True)
test_expr("1 & 1 & 0", False)
test_expr("1 & 1 | 0", True)
test_expr("1 -> 1 & 1 & 0", False)
test_expr("1 -> 0 | 1 & 0", False)
test_expr("1 <-> 1", True)

# test if & comes before |
test_expr("1 | 1 & 0", True)
