import numpy as np
import math

def F(x):
    return 1 / (1 + x)

def trapezoidal_rule(f, n,a,b):
    h = (a + b) / n
    integral_res = 0
    for x in np.arange(a, b, h):
        integral_res += (f(x-h) + f(x+h))*h/2
    return integral_res

print(trapezoidal_rule(F, 1000,0,1));