import numpy as np, string, random

def clean(txt):
    return ''.join(c for c in txt.upper() if c in string.ascii_uppercase)

def caesar_enc(txt, s):
    return ''.join(chr((ord(c)-65+s)%26+65) if c.isalpha() else c for c in txt.upper())

def caesar_dec(txt, s):
    return caesar_enc(txt, -s)

def mono_key(kw=None):
    if kw:
        seen, chars = set(), []
        for c in clean(kw):
            if c not in seen: seen.add(c); chars.append(c)
        for c in string.ascii_uppercase:
            if c not in seen: chars.append(c)
        return dict(zip(string.ascii_uppercase, chars))
    return dict(zip(string.ascii_uppercase, random.sample(string.ascii_uppercase, 26)))

def mono_enc(txt, key):
    return ''.join(key.get(c, c) for c in txt.upper())

def mono_dec(txt, key):
    return ''.join({v:k for k,v in key.items()}.get(c, c) for c in txt.upper())

def vig_enc(txt, key):
    txt, key = clean(txt), clean(key)
    return ''.join(chr((ord(txt[i])-65+ord(key[i%len(key)])-65)%26+65) for i in range(len(txt)))

def vig_dec(txt, key):
    txt, key = clean(txt), clean(key)
    return ''.join(chr((ord(txt[i])-65-ord(key[i%len(key)])+65)%26+65) for i in range(len(txt)))

def trans_enc(txt, key):
    txt, key = clean(txt), clean(key)
    pad = (len(key) - len(txt) % len(key)) % len(key)
    txt += 'X' * pad
    grid = np.array(list(txt)).reshape(-1, len(key))
    return ''.join(grid[:, np.argsort(list(key))].flatten('F'))

def trans_dec(txt, key):
    txt, key = clean(txt), clean(key)
    rows = len(txt) // len(key)
    grid = np.array(list(txt)).reshape(len(key), rows).T
    return ''.join(grid[:, np.argsort(np.argsort(list(key)))].flatten()).rstrip('X')

def play_matrix(key):
    key = clean(key).replace('J','I')
    seen, chars = set(), []
    for c in key:
        if c not in seen: seen.add(c); chars.append(c)
    for c in string.ascii_uppercase:
        if c != 'J' and c not in seen: chars.append(c)
    return np.array(chars).reshape(5,5)

def play_pos(m, c):
    r = np.where(m == c.replace('J','I'))
    return int(r[0][0]), int(r[1][0])

def play_enc(txt, key):
    txt, m = clean(txt).replace('J','I'), play_matrix(key)
    pairs, i = [], 0
    while i < len(txt):
        if i+1 < len(txt) and txt[i] != txt[i+1]:
            pairs.append(txt[i:i+2]); i += 2
        else:
            pairs.append(txt[i]+'X'); i += 1
    out = []
    for p in pairs:
        r1,c1 = play_pos(m, p[0])
        r2,c2 = play_pos(m, p[1])
        if r1 == r2: out += [m[r1,(c1+1)%5], m[r2,(c2+1)%5]]
        elif c1 == c2: out += [m[(r1+1)%5,c1], m[(r2+1)%5,c2]]
        else: out += [m[r1,c2], m[r2,c1]]
    return ''.join(out)

def play_dec(txt, key):
    txt, m = clean(txt).replace('J','I'), play_matrix(key)
    pairs = [txt[i:i+2] for i in range(0, len(txt), 2)]
    out = []
    for p in pairs:
        r1,c1 = play_pos(m, p[0])
        r2,c2 = play_pos(m, p[1])
        if r1 == r2: out += [m[r1,(c1-1)%5], m[r2,(c2-1)%5]]
        elif c1 == c2: out += [m[(r1-1)%5,c1], m[(r2-1)%5,c2]]
        else: out += [m[r1,c2], m[r2,c1]]
    return ''.join(out)

def adfgvx_enc(txt, pkey, tkey):
    txt = ''.join(c for c in txt.upper() if c in string.ascii_uppercase+"0123456789")
    alpha = string.ascii_uppercase + "0123456789"
    seen, chars = set(), []
    for c in pkey.upper():
        if c in alpha and c not in seen: seen.add(c); chars.append(c)
    for c in alpha:
        if c not in seen: chars.append(c)
    m, h = np.array(chars).reshape(6,6), ['A','D','F','G','V','X']
    sub = ''.join(h[int(np.where(m==c)[0][0])]+h[int(np.where(m==c)[1][0])] for c in txt)
    return trans_enc(sub, tkey)

def adfgvx_dec(txt, pkey, tkey):
    inter = trans_dec(txt, tkey)
    alpha = string.ascii_uppercase + "0123456789"
    seen, chars = set(), []
    for c in pkey.upper():
        if c in alpha and c not in seen: seen.add(c); chars.append(c)
    for c in alpha:
        if c not in seen: chars.append(c)
    m, h = np.array(chars).reshape(6,6), {c:i for i,c in enumerate(['A','D','F','G','V','X'])}
    return ''.join(m[h.get(inter[i],0), h.get(inter[i+1],0)] for i in range(0, len(inter)-1, 2))

def diana_enc(txt, key):
    txt, key = clean(txt), clean(key)
    return ''.join(chr((26-ord(txt[i])+65-ord(key[i%len(key)])+65)%26+65) for i in range(len(txt)))

def diana_dec(txt, key):
    return diana_enc(txt, key)
