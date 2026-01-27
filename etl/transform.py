import pandas as pd
from etl.encryption import get_cipher, encrypt_value
import yaml

with open("config/config.yaml") as f:
    config = yaml.safe_load(f)

cipher = get_cipher(config["security"]["encryption_key"])

def transform_data(df):
    df = df.dropna(subset=["transaction_id", "customer_id", "product_id", "quantity", "timestamp"])
    df = df[df["quantity"] > 0]

    df["customer_id"] = df["customer_id"].apply(lambda x: encrypt_value(x, cipher))
    df["product_id"] = df["product_id"].apply(lambda x: encrypt_value(x, cipher))

    df["sale_date"] = pd.to_datetime(df["timestamp"]).dt.date

    return df[["transaction_id", "customer_id", "product_id", "quantity", "sale_date"]]
