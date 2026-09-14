import numpy as np

# Fungsi untuk mencari Invers Modulo 26
def mod_inverse(a, m=26):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# Fungsi Enkripsi Hill Cipher
def encrypt(plaintext, K):
    plaintext = plaintext.upper().replace(" ", "")
    if len(plaintext) % 2 != 0:
        plaintext += 'X'  
    
    ciphertext = ""
    for i in range(0, len(plaintext), 2):
        p1 = ord(plaintext[i]) - 65
        p2 = ord(plaintext[i+1]) - 65
        P = np.array([[p1], [p2]])
        
        C = np.dot(K, P) % 26
        ciphertext += chr(C[0, 0] + 65) + chr(C[1, 0] + 65)
        
    return ciphertext

# Fungsi Dekripsi Hill Cipher
def decrypt(ciphertext, K):
    det = int(K[0, 0] * K[1, 1] - K[0, 1] * K[1, 0]) % 26
    det_inv = mod_inverse(det, 26)
    
    if det_inv is None:
        return "Matriks Kunci tidak memiliki invers modulo 26!"
    
    # Invers matriks 2x2 mod 26
    K_adj = np.array([[K[1, 1], -K[0, 1]], [-K[1, 0], K[0, 0]]]) % 26
    K_inv = (det_inv * K_adj) % 26
    
    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        c1 = ord(ciphertext[i]) - 65
        c2 = ord(ciphertext[i+1]) - 65
        C = np.array([[c1], [c2]])
        
        P = np.dot(K_inv, C) % 26
        plaintext += chr(int(P[0, 0]) + 65) + chr(int(P[1, 0]) + 65)
        
    return plaintext

# Fungsi Cari Kunci (Algebraic Approach + Fallback Brute Force)
def find_key(plaintext, ciphertext):
    plaintext = plaintext.upper().replace(" ", "")
    ciphertext = ciphertext.upper().replace(" ", "")
    
    n = len(plaintext)
    if n < 4:
        return "Panjang teks minimal 4 huruf!"
    
    # 1. METODE ALJABAR (Coba cari kombinasi blok yang memiliki invers mod 26)
    for i in range(0, n - 1, 2):
        for j in range(i + 2, n - 1, 2):
            p11 = ord(plaintext[i]) - 65
            p21 = ord(plaintext[i+1]) - 65
            p12 = ord(plaintext[j]) - 65
            p22 = ord(plaintext[j+1]) - 65
            
            P = np.array([[p11, p12], [p21, p22]])
            det_P = (p11 * p22 - p12 * p21) % 26
            det_P_inv = mod_inverse(det_P, 26)
            
            if det_P_inv is not None:
                c11 = ord(ciphertext[i]) - 65
                c21 = ord(ciphertext[i+1]) - 65
                c12 = ord(ciphertext[j]) - 65
                c22 = ord(ciphertext[j+1]) - 65
                
                C = np.array([[c11, c12], [c21, c22]])
                
                P_adj = np.array([[P[1, 1], -P[0, 1]], [-P[1, 0], P[0, 0]]]) % 26
                P_inv = (det_P_inv * P_adj) % 26
                
                K = np.dot(C, P_inv) % 26
                return K.astype(int)
                
    # 2. METODE BRUTE FORCE (Dijalankan jika metode aljabar gagal)
    print("\n[Info] Kombinasi invers matriks P tidak ditemukan. Menjalankan Brute Force Search...")
    
    P_vals = [ord(char) - 65 for char in plaintext]
    C_vals = [ord(char) - 65 for char in ciphertext]
    
    limit = min(len(P_vals), len(C_vals))
    if limit % 2 != 0:
        limit -= 1 
        
    for k11 in range(26):
        for k12 in range(26):
            for k21 in range(26):
                for k22 in range(26):
                    # Kunci harus memiliki invers mod 26 agar valid sebagai kunci Hill Cipher
                    det_K = (k11 * k22 - k12 * k21) % 26
                    if mod_inverse(det_K, 26) is None:
                        continue
                        
                    match = True
                    for idx in range(0, limit, 2):
                        p1, p2 = P_vals[idx], P_vals[idx+1]
                        c1, c2 = C_vals[idx], C_vals[idx+1]
                        
                        if (k11 * p1 + k12 * p2) % 26 != c1 or (k21 * p1 + k22 * p2) % 26 != c2:
                            match = False
                            break
                    
                    if match:
                        return np.array([[k11, k12], [k21, k22]], dtype=int)
                        
    return "Kunci tidak ditemukan (kemungkinan ada kesalahan pasangan Plaintext/Ciphertext)."

# Menu Utama
if __name__ == "__main__":
    print("=== PROGRAM HILL CIPHER 2x2 ===")
    print("1. Enkripsi")
    print("2. Dekripsi")
    print("3. Cari Kunci (Known Plaintext Attack)")
    pilihan = input("Pilih menu (1/2/3): ")

    if pilihan == '1':
        pt = input("Masukkan Plaintext: ")
        print("Masukkan Matriks Kunci 2x2 (4 angka dipisah spasi, ex: 7 6 2 5): ")
        k_vals = list(map(int, input().split()))
        K = np.array([[k_vals[0], k_vals[1]], [k_vals[2], k_vals[3]]])
        print("Ciphertext:", encrypt(pt, K))

    elif pilihan == '2':
        ct = input("Masukkan Ciphertext: ")
        print("Masukkan Matriks Kunci 2x2 (4 angka dipisah spasi, ex: 7 6 2 5): ")
        k_vals = list(map(int, input().split()))
        K = np.array([[k_vals[0], k_vals[1]], [k_vals[2], k_vals[3]]])
        print("Plaintext:", decrypt(ct, K))

    elif pilihan == '3':
        pt = input("Masukkan Plaintext (min. 4 huruf): ")
        ct = input("Masukkan Ciphertext (min. 4 huruf): ")
        K = find_key(pt, ct)
        print("\nMatriks Kunci yang Ditemukan:")
        
        if isinstance(K, np.ndarray):
            formatted_matrix = "\n ".join([str(row) for row in K]) 
            print(formatted_matrix)
        else:
            print(K)