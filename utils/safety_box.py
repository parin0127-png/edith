from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os 

load_dotenv()

def get_key():
    key = os.getenv("SAFETY_BOX_KEY")
    if not key:
        key = Fernet.generate_key().decode()
        with open(".env" , "a")as f:
            f.write(f"\n SAFETY_BOX_KEY = {key}")
    return key.encode()

def store_result(result):
    f = Fernet(get_key())
    encrypted = f.encrypt(result.encode())
    with open("safety_box.bin" , "wb")as f:
        f.write(encrypted)
    
def get_result():
    if not os.path.exists("safety_box.bin"):
        return None

    fernet = Fernet(get_key())
    with open("safety_box.bin", "rb")as f:
        encrypted = f.read()
    return fernet.decrypt(encrypted).decode()