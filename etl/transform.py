import pandas as pd
from etl.encryption import get_cipher, encrypt_value
import yaml

with open("config/config.yaml") as f:
    config = yaml.safe_load(f)

cipher = get_cipher(config["security"]["encryption_key"])
REQUIRED_COLUMNS = config["data_quality"]["required_columns"]
ENCRYPTED_COLUMNS = config["security"]["encrypted_columns"]
MIN_QUANTITY = config["data_quality"]["quantity_min"]
OUTPUT_COLUMNS = list(config["schema"]["output_columns"].keys())

def validate_schema(df, required_columns):
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def transform_data(df):
    # Schema validation (hard fail)
    validate_schema(df)

    # Drop rows with nulls in required columns
    df = df.dropna(subset=REQUIRED_COLUMNS)

    # Data quality rules
    df = df[df["quantity"] >= MIN_QUANTITY]

    # Encrypt sensitive columns (only if present)
    for col in ENCRYPTED_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(str).apply(
                lambda x: encrypt_value(x, cipher)
            )

    # Timestamp → sale_date
    df["sale_date"] = pd.to_datetime(df["timestamp"]).dt.date

    # Select only expected output columns (ignore extras)
    df = df[[col for col in OUTPUT_COLUMNS if col in df.columns]]

    return df
