from cryptography.fernet import Fernet

# Function to generate a new encryption key
def generate_key():
    """
    Generates a new encryption key using Fernet algorithm.
    
    Returns:
        bytes: A new Fernet encryption key
    """
    return Fernet.generate_key()

# Function to create a cipher object from an existing key
def get_cipher(key: str):
    """
    Creates a Fernet cipher object from a given encryption key.
    
    Args:
        key (str): The encryption key as a string
        
    Returns:
        Fernet: A cipher object ready to encrypt/decrypt data
    """
    return Fernet(key.encode())

# Function to encrypt a string value using a cipher
def encrypt_value(value: str, cipher) -> str:
    """
    Encrypts a string value using the provided cipher object.
    
    Args:
        value (str): The plaintext string to encrypt
        cipher: The Fernet cipher object to use for encryption
        
    Returns:
        str: The encrypted value as a string
    """
    return cipher.encrypt(value.encode()).decode()
