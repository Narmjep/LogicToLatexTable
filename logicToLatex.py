# Converts a series of logic statements to a latex truth table
# Inspired by https://github.com/davidcallanan/py-simple-math-interpreter
import sys
import re
import argparse
import numpy as np
from lexer import *
from tokenParser import *
from interpreter import *

def help():
    help = """
    logicToLatex.py
    Converts a series of logic statements to a latex truth table
    python logicToLatex.py [options] [formulas]
    Options:
    -h, --help: display help
    -i [input file], --input [input file]: input file. If this is specified, formulas will be read from the file instead of the command line
    -v, --verbose: verbose output

    Formulas:
    - Variables have to be alphanumeric and can be of any length. They are case sensitive. Example: A, a, A1, Megatron, etc.
    - Operators:
        - Negation: ! , can be put before a variable, operator or a formula. Example: !A, !(A & B), A !| B (nor), etc.
        - Conjunction: &
        - Disjunction: |
        - Implication: ->
        - Biconditional: <->
        - Exclusive or: +
        - Equivalence: =
        - Parentheses: ()
    - Example formulas: A, A & B, A | B, A -> B, A <-> B, ~(A & B), (A | B) -> C, etc.
    - You can separate formulas with a comma. Each formula will be displayed in a separate column in the truth table
    - When using the input file option, formulas can also be separated by a newline
    """
    print(help)

latex_table = r"""
\begin{tabular}{%s}
\hline
%s
\hline
\end{tabular}
"""

verbose = False

def formula_to_latex(formula):
    formula = f"$ {formula} $"
    formula = formula.replace("&", " \\land ")
    formula = formula.replace("|", " \\lor ")
    formula = formula.replace("->", " \\rightarrow ")
    formula = formula.replace("<->", " \\leftrightarrow ")
    formula = formula.replace("+", " \\oplus ")
    formula = formula.replace("=", " \\equiv ")
    formula = formula.replace("!", " \\lnot ")
    return formula

def print_verbose(*args):
    if verbose:
        print(*args)

def get_vars(formulas):
    vars = set()
    for formula in formulas:
        for char in formula:
            if char.isalnum():
                vars.add(char)
    return sorted(vars)

def generate_var_tuples(vars):
    tuples = []
    for i in range(2 ** len(vars)):
        tuples.append(list(np.binary_repr(i, width=len(vars))))
    return tuples

def solve_formula(formula, vars):
        lexer = Lexer(formula, vars)
        tokens = lexer.get_tokens()
        tree = Parser(tokens).parse()
        return Interpreter().visit(tree)


def main():
    argparser = argparse.ArgumentParser()
    argparser = argparse.ArgumentParser(add_help=False)
    argparser.add_argument("-h", "--help", help="display help", action="store_true")
    argparser.add_argument("-i", "--input", help="input file")
    argparser.add_argument("-v", "--verbose", help="verbose output", action="store_true")
    argparser.add_argument("formulas", nargs="*")
    args = argparser.parse_args()

    if args.help:
        help()
        sys.exit(0)

    if args.verbose:
        global verbose
        verbose = True

    formulas = []

    if args.input:
        #check if input file exists
        try:
            with open(args.input, "r") as f:
                formulas = f.readlines()
                formulas = [x.strip() for x in formulas]
        except FileNotFoundError:
            print("Error: input file not found")
            sys.exit(1)

    else:
        formulas = args.formulas
        formulas = ",".join(formulas).split(",")


    print_verbose("Formulas:")
    print_verbose("\n".join(formulas))

    # check for unwanted characters and print them if found
    for formula in formulas:
        for char in formula:
            if not char.isalnum() and char not in operator_chars and char not in ["(", ")", "!", " "]:
                print(f"Error: formula contains unwanted characters: {formula}")
                sys.exit(1)

    #Get variables
    vars = get_vars(formulas)



    print_verbose("Variables found:")
    print_verbose(vars)

    # Generate truth table : a dictionary where we store a list for every tuple. The list contains the truth value of each formula
    tuples = generate_var_tuples(vars)
    print_verbose("Variable tuples:")
    print_verbose(tuples)
    
    #list with size of number of tuples
    table = [0] * len(tuples)
    for i in range(len(tuples)):
        table[i] = []
        for formula in formulas:
            table[i].append(0)



    #Generate latex table
    
    header = "|" + "c|" * (len(formulas) + len(vars))
    lines = []
    # first line
    line = ""
    for var in vars:
        line = line + var + " & "
    # write formulas
    for formula in formulas:
        line = line + formula_to_latex(formula) + " & "

    line = line[:-2] + " \\\\ \n"
    lines.append(line)
    # second line
    lines.append("\\hline\n")
    # truth table
    for i in range(len(tuples)):
        line = ""
        for var in tuples[i]:
            line = line + var + " & "

        # solve formulas
        for j in range(len(formulas)):
            # vars
            vars_dict = {}
            vars_list = list(vars)
            for k in range(len(vars_list)):
                vars_dict[vars_list[k]] = tuples[i][k]
            print_verbose(f"Solving formula {formulas[j]} with vars {vars_dict}")
            table[i][j] = "1" if solve_formula(formulas[j], vars_dict) else "0"
            print_verbose("Result: ", table[i][j])
            line = line + str(table[i][j]) + " & "

        line = line[:-2] + " \\\\ \n"
        lines.append(line)
    
    global latex_table
    latex_table = latex_table % (header, "".join(lines))
    
    print(latex_table)
        


if __name__ == "__main__":
    main()