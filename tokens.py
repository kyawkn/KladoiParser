"""
File: tokens.py
Unit: tokens module. The token are defined as classes and tokenizing process happens here.
@author Kyaw Khant Nyar
"""
from collections import OrderedDict
import re


class TreeNode():
    successors = []
    predecessor = None


# Non Terminals objects
class Prog(TreeNode):
    pass


class Stmt(TreeNode):
    pass


class StmtSeq(TreeNode):
    pass


class StmtTail(TreeNode):
    pass


class Assign(TreeNode):
    pass


class Expr(TreeNode):
    pass


class IF(TreeNode):
    pass


class WHILE(TreeNode):
    pass


class ExtendedNode():
    pass


# Terminals , including keywords
class ID(ExtendedNode, TreeNode):
    data = None


class Literal(TreeNode, ExtendedNode):
    data = None


class Op(TreeNode, ExtendedNode):
    data = None


class ifkword(TreeNode):
    pass


class whilekword(TreeNode):
    pass


class beginkword(TreeNode):
    pass


class endkword(TreeNode):
    pass


class passkword(TreeNode):
    pass


class assignkword(TreeNode):
    pass


class comment(TreeNode):
    pass


class blanks(TreeNode):
    pass


# regex for the tokens
tokens = OrderedDict()
tokens[r'^\s+'] = blanks
tokens[r'^\|=.*?=\|'] = comment
tokens[r'^while\b'] = whilekword
tokens[r'^if\b'] = ifkword
tokens[r'^begin\b'] = beginkword
tokens[r'^end\b'] = endkword
tokens[r'^end$'] = endkword
tokens[r'^pass\b'] = passkword
tokens[r'^\s*:\s*=\s*'] = assignkword
tokens[r'^\-?\d+'] = Literal
tokens[r'^[\+\-\*\/]'] = Op
tokens[r'^[a-zA-Z]+'] = ID


def tokenize(input_str):
    """
    get the first token from the input string if result is found
    else return none
    :param input_str:
    """
    for key in tokens.keys():
        result = re.findall(key, input_str, re.DOTALL)
        if result:
            token = tokens[key]()
            # if token is a literal, id or Operator
            # their data is assigned
            if isinstance(token, ExtendedNode):
                token.data = input_str[:len(result[0])]
            return token, len(result[0])

    return None, None


def newline_counter(str):
    """
    :param str: input string
    :return: total number of newlines
    """
    return str.count('\n')
