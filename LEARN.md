# How I Built This Cryptography Portfolio

A step-by-step guide on building a cryptography learning tool for MTH 349.

---

## Step 1: Project Setup

First, I created the project structure and set up the development environment.

```bash
# Create project directory
mkdir cryp
cd cryp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install numpy pandas scipy
```

### Project Structure
```
cryp/
├── crypto_math.py      # Core math functions
├── classic_ciphers.py  # 7 classical ciphers
├── rsa_tool.py         # RSA encryption
├── analysis_tool.py    # Cryptanalysis tools
├── main.py             # Interactive menu
└── README.md           # Documentation
```

---

## Step 2: Building the Math Foundation (`crypto_math.py`)

The first module I built contains essential mathematical functions used by all ciphers.

### 2.1 Modular Exponentiation
Used for RSA encryption. Computes `(base^exp) mod m` efficiently.

```python
def mod_exp(base, exp, m):
    """Fast modular exponentiation using square-and-multiply."""
    result = 1
    base = base % m
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % m
        exp = exp >> 1
        base = (base * base) % m
    return result
```

### 2.2 Greatest Common Divisor (GCD)
Used to check if two numbers are coprime.

```python
def gcd(a, b):
    """Euclidean algorithm for GCD."""
    while b:
        a, b = b, a % b
    return a
```

### 2.3 Modular Inverse
Essential for RSA decryption. Finds `x` such that `(a * x) mod m = 1`.

```python
def mod_inv(a, m):
    """Extended Euclidean algorithm for modular inverse."""
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m
```

### 2.4 Primality Test
Used to generate RSA keys.

```python
def is_prime(n, k=10):
    """Miller-Rabin primality test."""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    # ... (Miller-Rabin implementation)
```

---

## Step 3: Implementing Classical Ciphers (`classic_ciphers.py`)

I implemented 7 classical ciphers, each demonstrating different cryptographic concepts.

### 3.1 Caesar Cipher
The simplest substitution cipher - shifts each letter by a fixed amount.

```python
def caesar_encrypt(plaintext, shift):
    """Shift each letter by 'shift' positions."""
    result = ""
    for char in plaintext.upper():
        if char.isalpha():
            result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        else:
            result += char
    return result
```

**Example:**
```
Input:  HELLO
Shift:  3
Output: KHOOR
```

### 3.2 Monoalphabetic Cipher
Uses a random permutation of the alphabet as the key.

### 3.3 Vigenère Cipher
A polyalphabetic cipher using a keyword.

```python
def vigenere_encrypt(plaintext, key):
    """Encrypt using Vigenère cipher."""
    result = ""
    key = key.upper()
    key_index = 0
    for char in plaintext.upper():
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            key_index += 1
        else:
            result += char
    return result
```

**Example:**
```
Plaintext: ATTACK
Key:       LEMON
Ciphertext: LXFOPV
```

### 3.4 Transposition Cipher
Rearranges letters based on a columnar pattern.

### 3.5 Playfair Cipher
Uses a 5x5 grid for digraph substitution.

### 3.6 ADFGVX Cipher
WWI German cipher combining substitution and transposition.

### 3.7 DIANA Cipher
NSA-developed cipher for field use.

---

## Step 4: Building RSA Encryption (`rsa_tool.py`)

RSA is a public-key cryptosystem. I implemented:

### 4.1 Key Generation
```python
def generate_keys(bits=512):
    """Generate RSA public and private keys."""
    # 1. Generate two large primes p, q
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    
    # 2. Compute n = p * q
    n = p * q
    
    # 3. Compute φ(n) = (p-1)(q-1)
    phi = (p - 1) * (q - 1)
    
    # 4. Choose e (commonly 65537)
    e = 65537
    
    # 5. Compute d = e^(-1) mod φ(n)
    d = mod_inv(e, phi)
    
    return (e, n), (d, n)  # public_key, private_key
```

### 4.2 Encryption & Decryption
```python
def rsa_encrypt(message, public_key):
    e, n = public_key
    return mod_exp(message, e, n)

def rsa_decrypt(ciphertext, private_key):
    d, n = private_key
    return mod_exp(ciphertext, d, n)
```

---

## Step 5: Cryptanalysis Tools (`analysis_tool.py`)

I built tools to analyze and break ciphers.

### 5.1 Frequency Analysis
Counts letter frequencies to break substitution ciphers.

```python
def frequency_table(text):
    """Count letter frequencies in text."""
    freq = {}
    for char in text.upper():
        if char.isalpha():
            freq[char] = freq.get(char, 0) + 1
    total = sum(freq.values())
    return {k: v/total for k, v in freq.items()}
```

### 5.2 Index of Coincidence
Helps determine Vigenère key length.

```python
def index_of_coincidence(text):
    """Calculate IC to detect polyalphabetic ciphers."""
    freq = frequency_table(text)
    n = len([c for c in text if c.isalpha()])
    ic = sum(f * (f * n - 1) for f in freq.values()) / (n * (n - 1))
    return ic
```

### 5.3 Entropy
Measures randomness of ciphertext.

```python
def entropy(text):
    """Shannon entropy of text."""
    freq = frequency_table(text)
    return -sum(p * math.log2(p) for p in freq.values() if p > 0)
```

---

## Step 6: Creating the Interactive Menu (`main.py`)

Finally, I built a user-friendly interface.

```python
def main():
    print("=== CRYPTO PORTFOLIO ===")
    print("1. All ciphers demo")
    print("2. Vigenere only")
    print("3. Vigenere freq tables")
    print("4. RSA only")
    print("5. Frequency analysis")
    
    choice = input("Option: ")
    # ... handle each option
```

---

## Step 7: Testing & Validation

I tested each component:

| Test | Input | Expected Output | ✓ |
|------|-------|-----------------|---|
| Caesar(3) | HELLO | KHOOR | ✓ |
| Vigenère(LEMON) | ATTACK | LXFOPV | ✓ |
| RSA encrypt/decrypt | 42 | 42 | ✓ |
| mod_exp(2,10,1000) | - | 24 | ✓ |

---

## What I Learned

1. **Modular arithmetic** is the foundation of modern cryptography
2. **Substitution ciphers** are vulnerable to frequency analysis
3. **RSA security** depends on the difficulty of factoring large numbers
4. **Key management** is critical - even strong algorithms fail with weak keys

---

## Requirements

- Python 3.8+
- numpy
- pandas  
- scipy

---

## How to Run

```bash
# Clone and setup
git clone https://github.com/dreuxx/cryp.git
cd cryp
python3 -m venv venv
source venv/bin/activate
pip install numpy pandas scipy

# Run
python main.py
```
