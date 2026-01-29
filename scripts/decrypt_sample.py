import sqlite3
import yaml
from cryptography.fernet import Fernet

# Load config (non-sensitive)
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Load secrets (not versioned)
with open("config/secrets.yaml", "r") as f:
    secrets = yaml.safe_load(f)

DB_PATH = config["database"]["url"].replace("sqlite:///", "")
ENCRYPTION_KEY = secrets["security"]["encryption_key"].encode()
ENCRYPTED_COLUMNS = config["security"]["encrypted_columns"]

cipher = Fernet(ENCRYPTION_KEY)

def decrypt_row(row, col_indexes):
    row = list(row)
    for idx in col_indexes:
        row[idx] = cipher.decrypt(row[idx].encode()).decode()
    return tuple(row)

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = f"""
        SELECT transaction_id, {", ".join(ENCRYPTED_COLUMNS)}
        FROM sales
        LIMIT 10
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    print("\nDecrypted sample rows:\n")

    encrypted_indexes = list(range(1, len(ENCRYPTED_COLUMNS) + 1))

    for row in rows:
        print(decrypt_row(row, encrypted_indexes))

    conn.close()

if __name__ == "__main__":
    main()
