# File phyllomaker.py
# Unit phyllomaker module, that prints phyllo code from the syntax tree
# @author Kyaw Khant Nyar

from tokens import *


def make(tree: TreeNode):
    """
    make the phyllo code from the syntax tree
    :param tree: syntax tree
    """
    _, phyllo = visit_tree(tree)
    print(phyllo)


def visit_assign(tree: TreeNode):
    """
    visit the tree for the assign
    rule: id assignkword expression
    :param tree: part of syntax tree
    :return: current phyllo code line number, phyllo code
    """
    linenum, phyllo = visit_expr(tree.successors[-1])
    phyllo += "STORE {}\n".format(tree.successors[0].data)
    return linenum + 1, phyllo


def visit_op(tree: TreeNode):
    """
    visit the tree for the assign
    rule: id assignkword expression
    :param tree: part of syntax tree
    :return: current phyllo code line number, phyllo code
    """
    llinenum, lstr = visit_expr(tree.successors[1])
    rlinenum, rstr = visit_expr(tree.successors[2])
    phyllo = lstr + rstr + tree.successors[0].data + "\n"
    linenum = llinenum + rlinenum + 1
    return linenum, phyllo


def visit_id(tree):
    """
    :param tree: part of syntax tree
    :return: current phyllo code line number, phyllo code
    """
    phyllo = "LOAD {}\n".format(tree.data)
    return 1, phyllo


def visit_lit(tree):
    """
    :param tree: part of syntax tree
    :return: current phyllo code line number, phyllo code
    """
    phyllo = "PUSH {}\n".format(tree.data)
    return 1, phyllo


def visit_expr(tree: TreeNode):
    """
    visit the tree for the expression
    rule: op expression expression
    :param tree: part of syntax tree
    :return: current phyllo code line number, phyllo code
    """
    for child in tree.successors:
        if isinstance(child, Literal):
            return visit_lit(child)

        if isinstance(child, ID):
            return visit_id(child)

        if isinstance(child, Op):
            return visit_op(child.predecessor)


def visit_while(tree: TreeNode):
    """
    visit the tree for the while
    rule: while expression prog
   :param tree: part of syntax tree
    :return: current phyllo code line number, phyllo code
    """
    exp_linenum, exp_str = visit_expr(tree.successors[1])
    prog_linenum, prog_str = visit_tree(tree.successors[2])
    while_linenum = prog_linenum + 2
    while_str = "BRZ +{}\n".format(while_linenum)
    jump_linenum = while_linenum + exp_linenum - 1
    jump_str = "JUMP -{}\n".format(jump_linenum)

    phyllo = exp_str + while_str + prog_str + jump_str
    return jump_linenum + 1, phyllo


def visit_if(tree: TreeNode):
    """
    visit the tree for the if
    rule: if expression prog prog
    :param tree: part of syntax tree
    :return: current phyllo code line number, phyllo code
    """
    exp_linenum, exp_str = visit_expr(tree.successors[1])
    left_linenum, left_str = visit_tree(tree.successors[2])
    right_linenum, right_str = visit_tree(tree.successors[3])
    linenum = left_linenum + 1
    if_str = "BRZ +{}\n".format(linenum)
    phyllo = exp_str + if_str + left_str + right_str

    return linenum + right_linenum + exp_linenum, phyllo


def visit_tree(tree: TreeNode):
    """
    visit tree check the current node and run process based on their
    types
    :param tree: syntax tree
    :return: current phyllo code line number, phyllo code
    """
    linenum = 0
    phyllo = ""
    for child in tree.successors:

        # check the types and visit their part of the tree
        if isinstance(child, Assign):
            temp, str = visit_assign(child)

        elif isinstance(child, IF):
            temp, str = visit_if(child)

        elif isinstance(child, WHILE):
            temp, str = visit_while(child)

        else:
            temp, str = visit_tree(child)

        # increment the line number
        linenum += temp
        # add phyllo codes
        phyllo += str

    return linenum, phyllo
