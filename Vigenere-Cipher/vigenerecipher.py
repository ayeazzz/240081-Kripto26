def vigenere_encrypt(plaintext, key):
    plaintext = plaintext.upper().replace(" ", "")
    key = key.upper().replace(" ", "")
    ciphertext = ""
    
    for i in range(len(plaintext)):
        p = ord(plaintext[i]) - 65
        k = ord(key[i % len(key)]) - 65 
        c = (p + k) % 26
        ciphertext += chr(c + 65)
        
    return ciphertext

def vigenere_decrypt(ciphertext, key):
    ciphertext = ciphertext.upper().replace(" ", "")
    key = key.upper().replace(" ", "")
    plaintext = ""
    
    for i in range(len(ciphertext)):
        c = ord(ciphertext[i]) - 65
        k = ord(key[i % len(key)]) - 65
        p = (c - k) % 26
        plaintext += chr(p + 65)
        
    return plaintext

def vigenere_find_key(plaintext, ciphertext):
    plaintext = plaintext.upper().replace(" ", "")
    ciphertext = ciphertext.upper().replace(" ", "")
    
    # Memastikan panjang teks sama agar akurat
    if len(plaintext) != len(ciphertext):
        return "Error: Panjang Plaintext dan Ciphertext harus sama untuk mencari Key."
        
    key = ""
    for i in range(len(plaintext)):
        p = ord(plaintext[i]) - 65
        c = ord(ciphertext[i]) - 65
        # Rumus mencari Key: (C - P) mod 26
        k = (c - p) % 26
        key += chr(k + 65)
        
    return key

def main():
    while True:
        print("=== PROGRAM VIGENERE CIPHER ===")
        print("1. Enkripsi (Plaintext -> Ciphertext)")
        print("2. Dekripsi (Ciphertext -> Plaintext)")
        print("3. Cari Key")
        print("4. Keluar")
        
        pilihan = input("Pilih menu (1/2/3/4): ")
        
        if pilihan == '1':
            print("\n-- Menu Enkripsi --")
            pt = input("Masukkan Plaintext: ")
            key = input("Masukkan Key      : ")
            hasil = vigenere_encrypt(pt, key)
            print(f"Hasil Enkripsi    : {hasil}")
            
        elif pilihan == '2':
            print("\n-- Menu Dekripsi --")
            ct = input("Masukkan Ciphertext: ")
            key = input("Masukkan Key       : ")
            hasil = vigenere_decrypt(ct, key)
            print(f"Hasil Dekripsi     : {hasil}")
            
        elif pilihan == '3':
            print("\n-- Menu Cari Key --")
            pt = input("Masukkan Plaintext : ")
            ct = input("Masukkan Ciphertext: ")
            hasil = vigenere_find_key(pt, ct)
            print(f"Key yang ditemukan : {hasil}")
            
        elif pilihan == '4':
            print("\nTerima kasih telah menggunakan program ini!")
            break
            
        else:
            print("\nPilihan tidak valid. Silakan pilih 1, 2, 3, atau 4.")

if __name__ == "__main__":
    main()