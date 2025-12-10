from crypto_math import mod_exp, gcd, mod_inv, is_prime
from classic_ciphers import *
from rsa_tool import gen_keys, enc, dec
from analysis_tool import freq, adj, entropy, entropy2, vig_freq

def main():
    print("\n=== CRYPTO PORTFOLIO ===")
    print("1. All ciphers demo")
    print("2. Vigenere only (1.9.9)")
    print("3. Vigenere freq tables (1.9.10)")
    print("4. RSA only")
    print("5. Frequency analysis")
    
    opt = input("\nOption: ").strip() or "1"
    
    if opt == "1":
        msg = input("Text: ").strip() or "HELLOWORLD"
        key = input("Key: ").strip() or "SECRET"
        print(f"\nInput: {msg} | Key: {key}\n")
        
        print("MATH:")
        print(f"  mod_exp(3,5,7)={mod_exp(3,5,7)}, gcd(48,18)={gcd(48,18)}, mod_inv(3,11)={mod_inv(3,11)}")
        
        print("\nCIPHERS:")
        for name, e, d in [
            ("Caesar", caesar_enc(msg,3), caesar_dec(caesar_enc(msg,3),3)),
            ("Vigenere", vig_enc(msg,key), vig_dec(vig_enc(msg,key),key)),
            ("Trans", trans_enc(msg,key), trans_dec(trans_enc(msg,key),key)),
            ("Playfair", play_enc(msg,key), play_dec(play_enc(msg,key),key)),
            ("Diana", diana_enc(msg,key), diana_dec(diana_enc(msg,key),key)),
        ]:
            print(f"  {name}: {e} -> {d}")
    
    elif opt == "2":
        # 1.9.9 Vigenere Encrypt/Decrypt
        print("\n--- 1.9.9 VIGENERE ---")
        msg = input("Text: ").strip() or "ATTACKATDAWN"
        key = input("Key: ").strip() or "LEMON"
        mode = input("(e)ncrypt or (d)ecrypt? ").strip().lower() or "e"
        
        if mode == "e":
            result = vig_enc(msg, key)
            print(f"\nPlaintext:  {clean(msg)}")
            print(f"Key:        {clean(key)}")
            print(f"Ciphertext: {result}")
        else:
            result = vig_dec(msg, key)
            print(f"\nCiphertext: {clean(msg)}")
            print(f"Key:        {clean(key)}")
            print(f"Plaintext:  {result}")
    
    elif opt == "3":
        # 1.9.10 Vigenere Frequency Tables
        print("\n--- 1.9.10 VIGENERE FREQ TABLES ---")
        cipher = input("Ciphertext: ").strip() or "LXFOPVEFRNHR"
        k = int(input("Key length k: ").strip() or "3")
        
        tables = vig_freq(cipher, k)
        print(f"\nCiphertext: {clean(cipher)}")
        print(f"Key length: {k}")
        print("-" * 40)
        
        for t in tables:
            print(f"\nPosition {t['pos']}: chars at 0,{k},{2*k},... = {t['group']}")
            print(f"  IC = {t['IC']:.4f} (English~0.067, Random~0.038)")
            print(f"  Flatness = {t['flat']:.2%} (0%=English, 43%=Random)")
            print(f"  Top letters: {list(t['freq'].head(3)['Letter'])}")
    
    elif opt == "4":
        print("\n--- RSA ---")
        msg = input("Text: ").strip() or "HELLO"
        bits = int(input("Bits (64): ").strip() or "64")
        pub, priv = gen_keys(bits)
        c = enc(msg, pub)
        d_msg = dec(c, priv)
        print(f"\nOriginal: {msg}")
        print(f"Encrypted: {c[:2]}...")
        print(f"Decrypted: {d_msg}")
    
    elif opt == "5":
        print("\n--- FREQUENCY ANALYSIS ---")
        txt = input("Text: ").strip() or "THE QUICK BROWN FOX"
        print(f"\nEntropy: {entropy(txt):.4f} bits")
        freq(txt, latex=True)
    
    print("\nDone!")

if __name__ == "__main__":
    main()
