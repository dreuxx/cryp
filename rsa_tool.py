from crypto_math import mod_exp, mod_inv, gen_prime, gcd

def gen_keys(bits=512):
    p, q = gen_prime(bits), gen_prime(bits)
    n, phi = p * q, (p-1) * (q-1)
    e = 65537
    if gcd(e, phi) != 1:
        e = 3
        while gcd(e, phi) != 1: e += 2
    d = mod_inv(e, phi)
    return (e, n), (d, n)

def enc(msg, pub):
    e, n = pub
    return [mod_exp(ord(c), e, n) for c in msg]

def dec(cipher, priv):
    d, n = priv
    return ''.join(chr(mod_exp(c, d, n)) for c in cipher)

def sign(msg, priv):
    d, n = priv
    return [mod_exp(ord(c), d, n) for c in msg]

def verify(msg, sig, pub):
    e, n = pub
    return ''.join(chr(mod_exp(s, e, n)) for s in sig) == msg
