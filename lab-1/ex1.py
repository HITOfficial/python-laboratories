#  variables: a-z
import string
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


# print(check('(a)>(b&c)'))
# print(check('a>b>c&a'))


# ONP

# a|b|c ab|c|
# a|(b|c) abc||

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


def val(expr):
    pass


print(onp('(a>(b|c))'))
