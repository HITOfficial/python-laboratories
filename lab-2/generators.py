# iterators / generators


def dividers(n):
    for i in range(1, n):
        if n % i == 0:
            yield i


def fib_gen():
    a, b = 0, 1
    while True:
        a, b = b, a+b
        yield a


def primes_gen():
    n = 3
    prime_list = [2, 3]
    yield 2
    yield 3
    while True:
        n += 2
        for p in prime_list:
            if n % p == 0 and n**0.5 <= p:
                break
        # execute only if not broke for
        else:
            prime_list.append(n)
            yield n


def twins_primes():
    g = primes_gen()
    yield 3, 5
    while True:
        a = next(g)
        b = next(g)
        if b-a == 2:
            yield a, b


# generator like table of truth
def rec_gen(n):
    if n == 0:
        yield ""
    else:
        for c in rec_gen(n-1):
            yield "0"+c
            yield "1"+c


# permutations generator
def perm_gen(s):
    if len(s) == 1:
        yield s
    else:
        for p in perm_gen(s[:-1]):
            for i in range(len(s)):
                # all combinations
                yield p[:i] + s[-1] + p[i:]


def combinations_gen(s, k):
    if k == 1:
        for el in s:
            yield el
    elif len(s) == k:
        yield s
    else:
        for el in combinations_gen(s[:-1], k-1):
            yield el + s[-1]
        for el in combinations_gen(s[:-1], k):
            yield el


# variations
def variations_gen(s, k):
    for el in combinations_gen(s, k):
        for el2 in perm_gen(el):
            yield el2
