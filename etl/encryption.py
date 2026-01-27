from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def get_cipher(key: str):
    return Fernet(key.encode())

def encrypt_value(value: str, cipher) -> str:
    return cipher.encrypt(value.encode()).decode()
