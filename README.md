# Cryptography Portfolio

A simple Python project for learning cryptography. Made for MTH 349.

## What is this?

This project has:
- **4 math functions**: modular exponentiation, GCD, modular inverse, primality test
- **7 classic ciphers**: Caesar, Monoalphabetic, Vigenère, Transposition, Playfair, ADFGVX, DIANA
- **RSA**: public-key encryption
- **Analysis tools**: frequency tables, adjacency tables, entropy

## Install

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/cryp.git
cd cryp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install numpy pandas scipy
```

## How to use

```bash
# Activate environment
source venv/bin/activate

# Run the program
python main.py
```

Then choose an option:
```
=== CRYPTO PORTFOLIO ===
1. All ciphers demo
2. Vigenere only
3. Vigenere freq tables
4. RSA only
5. Frequency analysis

Option: 
```

## Example

```
Option: 2
Text: ATTACK
Key: LEMON
(e)ncrypt or (d)ecrypt? e

Ciphertext: LXFOPV
```

## Files

| File | Description |
|------|-------------|
| `crypto_math.py` | Math functions (mod_exp, gcd, mod_inv, is_prime) |
| `classic_ciphers.py` | 7 classic ciphers |
| `rsa_tool.py` | RSA encryption |
| `analysis_tool.py` | Frequency and entropy analysis |
| `main.py` | Main menu program |

## Requirements

- Python 3.8+
- numpy
- pandas
- scipy
