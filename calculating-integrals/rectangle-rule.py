import numpy as np


def F(x):
    return 1 / (1 + x)


def rectangle_rule(f, n, a, b):
    h = (a + b) / n
    integral_res = 0
    for x in np.arange(a, b, h):
        integral_res += f(x) * h
    return integral_res


print(rectangle_rule(F, 1000, 0, 1));
print(rectangle_rule(F, 3, 0, 1));
print(rectangle_rule(F, 5, 0, 1));
