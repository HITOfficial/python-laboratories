#  variables: a-z
from cmath import exp
from re import L
import string
from textwrap import indent
variables = string.ascii_lowercase
# & | >
# ()
# ~ -> 4
# ^ -> 3
# & | -> 2
# > 1

n = ['~']
p = ['^']
c = ['&', '|']
e = ['>']


def check(expression):
    operands = ['|', '&', '>']
    state = True
    brackets = 0

    if expression == "":
        return False
    for s in expression:
        if state:
            if s in variables:
                state = False
            elif s in operands:
                return False
        else:
            if s in operands:
                return True
            elif s in variables or s == '(':
                return False
            if s == '(':
                brackets += 1
            if s == ')':
                brackets -= 1
            if brackets < 0:
                return False
            if not s in variables or s not in operands and operands not in ['(', ')']:
                return False
    return brackets == 0 and not state


def onp(expr):
    while expr[0] == '(' and expr[-1] == ')' and check(expr[1:-1]):
        expr = expr[1:-1]
    p = bal(expr, '>')
    if p >= 0:
        return onp(expr[:p]) + onp(expr[p+1:]) + expr[p]
    p = bal(expr, "|&")
    if p >= 0:
        return onp(expr[:p]) + onp(expr[p+1:]) + expr[p]
    return expr


def bal(expr, op):
    brackets = 0
    for i in range(len(expr)-1, -1, -1):
        if expr[i] == '(':
            brackets += 1
        if expr[i] == ')':
            brackets -= 1
        if expr[i] in op and len(expr) > 0:
            return i
    return -1


def var(expr):
    "".join(list(set(expr) and set(variables)))


def gen(n):
    # using binary mask creating all possibilities
    possibilities = 2**n
    array = [[0]*n for _ in range(possibilities)]
    for i in range(possibilities):
        position = n-1
        i_cpy = i
        while position >= 0:
            array[i_cpy][position] = i % 2
            i //= 2
            position -= 1
    return array


def map(expr, vec):
    result = ""
    vec_pos = 0
    for s in expr:
        # variable
        if s in variables:
            result += vec[vec_pos]
            vec_pos += 1
        # operand
        else:
            result += s
    return result


def check_expr(expr):
    if len(expr) == 3:
        # print(expr[0], expr[1], expr[0] and expr[1])
        if expr[2] == "&":
            return int(int(expr[0]) and int(expr[1]))
        elif expr[2] == "|":
            return int(int(expr[0]) or int(expr[1]))
        else:
            # p=>q == ~(p and ~ q)
            return int(not(int(expr[0]) and not int(expr[1])))
    else:
        return int(int(expr[0]))


def val(expr):
    while len(expr) > 1:
        formula = expr[0]
        flag = 0
        formula += expr[1]
        idx = 0
        if "&" in expr:
            idx = expr.index("&")
            formula += expr[idx]
            flag = 1
        if not flag and "|" in expr:
            idx = expr.index("|")
            formula += expr[idx]
            flag = 1
        if not flag and ">" in expr:
            idx = expr.index(">")
            formula += expr[idx]
        expr = expr[2:idx] + expr[idx+1:]
        expr = str(check_expr(formula)) + expr
    return bool(int(expr))


def tautology(expr):
    n = 0
    for el in expr:
        if el in variables:
            n += 1
    # array of possibilites to check
    possibilities = gen(n)
    for i in range(len(possibilities)):
        logical_expr = map(expr, "".join([str(el) for el in possibilities[i]]))
        if not val(logical_expr):
            return False
    return True


print(tautology("abc|>"))
