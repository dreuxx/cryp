import pandas as pd, numpy as np, string
from scipy.stats import entropy as sp_entropy
from collections import Counter

def clean(txt):
    return ''.join(c for c in txt.upper() if c in string.ascii_uppercase)

def freq(txt, latex=False):
    txt = clean(txt)
    s = pd.Series(list(txt))
    df = s.value_counts().reset_index()
    df.columns = ['Letter', 'Count']
    df['%'] = (df['Count'] / len(txt) * 100).round(2)
    if latex:
        print("\\begin{tabular}{lrr}\n\\toprule\nLetter & Count & \\% \\\\\\midrule")
        for _, r in df.iterrows(): print(f"{r['Letter']} & {r['Count']} & {r['%']:.2f} \\\\")
        print("\\bottomrule\n\\end{tabular}")
    return df

def adj(txt, top=3):
    txt = clean(txt)
    pairs = [(txt[i], txt[i+1]) for i in range(len(txt)-1)]
    df = pd.DataFrame(pairs, columns=['L1','L2'])
    cross = pd.crosstab(df['L1'], df['L2'])
    cnt = Counter(txt)
    out = []
    for l in sorted(cnt, key=cnt.get, reverse=True):
        pre = df[df['L2']==l]['L1'].value_counts().head(top).index.tolist()
        post = df[df['L1']==l]['L2'].value_counts().head(top).index.tolist()
        out.append({'Pre': ','.join(pre), 'L': l, 'Post': ','.join(post)})
    return pd.DataFrame(out), cross

def entropy(txt):
    txt = clean(txt)
    probs = pd.Series(list(txt)).value_counts(normalize=True)
    return sp_entropy(probs, base=2)

def entropy2(txt):
    txt = clean(txt)
    bigrams = [txt[i:i+2] for i in range(len(txt)-1)]
    probs = pd.Series(bigrams).value_counts(normalize=True)
    return sp_entropy(probs, base=2)

def vig_freq(cipher, k):
    """
    1.9.10: Split ciphertext into k groups and return frequency + flatness for each.
    Flatness is measured by Index of Coincidence (IC).
    English IC ≈ 0.067, Random IC ≈ 0.038
    """
    cipher = clean(cipher)
    tables = []
    for i in range(k):
        group = cipher[i::k]  # c_i, c_{i+k}, c_{i+2k}, ...
        if not group:
            continue
        counts = Counter(group)
        total = len(group)
        # Index of Coincidence = sum(n*(n-1)) / (N*(N-1))
        ic = sum(n*(n-1) for n in counts.values()) / (total*(total-1)) if total > 1 else 0
        df = pd.DataFrame([{'Letter': l, 'Count': c, '%': c/total*100} for l, c in counts.most_common()])
        tables.append({'pos': i, 'group': group, 'freq': df, 'IC': ic, 'flat': 1-ic/0.067})
    return tables

