import pandas as pd

def transform_data(df):
    # Drop missing critical fields
    df = df.dropna(subset=["transaction_id", "customer_id", "product_id", "quantity", "timestamp"])

    # Remove invalid quantities
    df = df[df["quantity"] > 0]

    # Convert timestamp to date
    df["sale_date"] = pd.to_datetime(df["timestamp"]).dt.date

    return df[["transaction_id", "customer_id", "product_id", "quantity", "sale_date"]]
