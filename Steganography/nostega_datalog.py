import csv
import datetime
import random
import os

def encode_nostega(message, output_file):
    """
    Mengubah pesan menjadi file CSV log suhu mesin.
    Karakter diubah menjadi nilai ASCII dan ditambahkan ke base suhu.
    """
    base_temp = 100  
    start_time = datetime.datetime.now()
    
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Sensor_ID", "Temperature_C"])
        
        for i, char in enumerate(message):
            ascii_val = ord(char)
            temp = base_temp + ascii_val

            current_time = start_time + datetime.timedelta(minutes=5*i)
            time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
            sensor_id = f"SENS-{random.randint(1000, 9999)}"
            
            writer.writerow([time_str, sensor_id, temp])
            
    print(f"\n[SUCCESS] Pesan berhasil di-encode!")
    print(f"File log palsu telah dibuat: {os.path.abspath(output_file)}")

def decode_nostega(input_file):
    """
    Mengekstrak pesan dari file CSV log suhu mesin.
    """
    message = ""
    base_temp = 100
    
    try:
        with open(input_file, 'r') as file:
            reader = csv.reader(file)
            next(reader) 
            
            for row in reader:
                temp = int(row[2])
                ascii_val = temp - base_temp
                message += chr(ascii_val)
                
        return message
    except FileNotFoundError:
        return "Error: File tidak ditemukan."
    except Exception as e:
        return f"Error saat membaca file: {e}"

# ==== Menu Utama Program ====
if __name__ == "__main__":
    print("=== Program NoStega (Data Log Generator) ===")
    pilihan = input("Pilih mode (1: Encode, 2: Decode): ")
    
    if pilihan == '1':
        pesan = input("Masukkan pesan rahasia: ")
        file_out = input("Masukkan nama file output (contoh: log_mesin.csv): ")
        

        if not file_out.endswith('.csv'):
            file_out += '.csv'
            
        encode_nostega(pesan, file_out)
        
    elif pilihan == '2':
        file_in = input("Masukkan nama file CSV yang ingin di-decode (contoh: log_mesin.csv): ")
        pesan_rahasia = decode_nostega(file_in)
        print(f"\n[HASIL DECODE] Pesan Rahasia: {pesan_rahasia}")
        
    else:
        print("Pilihan tidak valid.")