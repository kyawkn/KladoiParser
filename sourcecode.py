# File: sourcecode.py
# Unit: class sourcecode module that prints the kladoi
# code back from the
# abstract syntax tree

from tokens import *

keyword_dict = {
    whilekword: "while ",
    endkword: "end ",
    ifkword: "if ",
    passkword: "pass ",
    assignkword: ":= ",
    beginkword: "begin ",

}


def print_kladoi(tree, tabs=0):
    """
    print the kladoi code back
    :param tree: abstract syntax tree
    :param tabs: number of tabs to add
    """
    if tree is None:
        return

    if isinstance(tree, Stmt):
        # check if its the root node
        if tree.predecessor.predecessor is not None:
            print()
            print("\t" * tabs, end="")

    if not tree.successors:
        if isinstance(tree, whilekword) or isinstance(tree, endkword):
            print()
            print("\t" * tabs, end="")

        if isinstance(tree, StmtTail):
            pass
        elif type(tree) in keyword_dict:
            print(keyword_dict[type(tree)], end="")
        else:
            print(tree.data, end=" ")

    for i in range(len(tree.successors)):
        temp_tabs = tabs

        if isinstance(tree, IF):
            if i == 2:
                temp_tabs += 1

        if isinstance(tree, WHILE):
            if i == 2:
                temp_tabs += 1

        print_kladoi(tree.successors[i], temp_tabs)

