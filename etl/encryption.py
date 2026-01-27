from cryptography.fernet import Fernet

def get_cipher(key: str):
    return Fernet(key.encode())

def encrypt_value(value: str, cipher) -> str:
    return cipher.encrypt(value.encode()).decode()
