# File: main.py
# Unit: main module
# @author Kyaw Khant Nyar


from tokens import *
import rules
import sys
from phyllomaker import make
from sourcecode import print_kladoi


def parser(input_prog):
    """
    the parser take in the desired input program and return
    the abstract tree
    """
    prog = Prog()
    stack = [prog]
    line_count = 1
    # check as long as there is something in the stack
    while stack:
        token, length = tokenize(input_prog)

        if token is None:
            raise ValueError("Line{}: Syntax Error".format(line_count))

        # process the comments
        if type(token) is comment or type(token) is blanks:
            line_count += newline_counter(input_prog[:length])
            input_prog = input_prog[length:]
            continue

        popped = stack.pop()
        if type(popped) == type(token):
            line_count += newline_counter(input_prog[:length])
            input_prog = input_prog[length:]
            if isinstance(popped, ExtendedNode):
                popped.data = token.data
            continue

        try:
            reduced = rules.rule_reduce(type(popped), type(token))
            popped.successors = reduced
            for successor in reduced:
                successor.predecessor = popped
        except:
            raise ValueError("Line {}: Syntax Error".format(line_count))
        stack.extend(reversed(reduced))

    while input_prog:
        token, len = tokenize(input_prog)
        if type(token) is comment or type(token) is blanks:
            line_count += newline_counter(input_prog[:length])
            input_prog = input_prog[length:]
            continue
        raise ValueError(
            "Extra codes at end of the program"
        )

    return prog

# main file
if __name__ == '__main__':
    # if no file is provided
    # get from the stdin
    if len(sys.argv) == 2:
        file1 = open(sys.argv[1], "r+")
        input_str = file1.read()
        astree = parser(input_str)
        print_kladoi(astree)
        print("\n")
        make(astree)
    else:
        input_str = sys.stdin.read()
        astree = parser(input_str)
        print_kladoi(astree)
        print("\n")
        make(astree)