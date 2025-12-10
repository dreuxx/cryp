import math, random

def mod_exp(a, k, n):
    return pow(a, k, n)

def gcd(a, b):
    return math.gcd(a, b)

def mod_inv(a, n):
    return pow(a, -1, n)

def is_prime(n, k=10):
    if n < 2: return False
    if n == 2 or n == 3: return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else:
            return False
    return True

def gen_prime(bits=512):
    while True:
        p = random.getrandbits(bits) | (1 << bits - 1) | 1
        if is_prime(p): return p
