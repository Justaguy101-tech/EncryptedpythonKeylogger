from cryptography.fernet import Fernet
import os

with open("secret.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

log_files = [f for f in os.listdir() if f.startswith("log_") and f.endswith(".txt")]
filename = max(log_files, key=os.path.getctime)

output_file = "decrypted_" + filename

with open(filename, "rb") as enc_file, open(output_file, "w", encoding="utf-8") as dec_file:
    for line in enc_file:
        try:
            decrypted = fernet.decrypt(line.strip()).decode()
            print(decrypted)
            dec_file.write(decrypted + "/n")
        except Exception as e:
            print("[!] Coudn't decrypt a line:", e)