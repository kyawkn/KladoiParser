"""
File: rules.py
Unit: rules module for parse table and all set of possible rules
@author Kyaw Khant Nyar
"""
from tokens import *

# the parse table
rules = (
    {
        Prog: {
            beginkword: [beginkword, StmtSeq, endkword],
            passkword: [Stmt],
            ID: [Stmt],
            ifkword: [Stmt],
            whilekword: [Stmt]
        },
        StmtSeq: {
            passkword: [Stmt, StmtTail, StmtTail],
            ID: [Stmt, StmtTail, StmtTail],
            ifkword: [Stmt, StmtTail, StmtTail],
            whilekword: [Stmt, StmtTail, StmtTail],
        },
        StmtTail: {
            # if tail is end its just empty
            endkword: [],
            passkword: [StmtSeq],
            ID: [StmtSeq],
            ifkword: [StmtSeq],
            whilekword: [WHILE]

        },
        Stmt: {
            passkword: [passkword],
            ID: [Assign],
            ifkword: [IF],
            whilekword: [WHILE]
        },
        Assign: {
            ID: [ID, assignkword, Expr]
        },
        IF: {
            ifkword: [ifkword, Expr, Prog, Prog]
        },
        WHILE: {
            whilekword: [whilekword, Expr, Prog]
        },
        Expr: {
            ID: [ID],
            Literal: [Literal],
            Op: [Op, Expr, Expr]
        }

    }
)


def rule_reduce(rule, token):
    """
    uses the parse table to decide the rules of the given toke and rule
    :param rule:
    :param token:
    :return:
    """
    draft_rules = rules[rule]
    token_rules = draft_rules[token]
    reduced_rules = []
    for r in token_rules:
        reduced_rules.append(r())

    return reduced_rules
