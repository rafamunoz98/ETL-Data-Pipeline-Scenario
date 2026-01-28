from sqlalchemy import create_engine, text
from concurrent.futures import ThreadPoolExecutor
import math
import yaml

with open("config/config.yaml") as f:
    config = yaml.safe_load(f)

TABLE = config["database"]["table"]
BATCH_SIZE = config["etl"]["batch_size"]
INCREMENTAL_KEY = config["etl"]["incremental_key"]

engine = create_engine(
    "sqlite:///sales.db",
    connect_args={"check_same_thread": False}
)


def init_db():
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS sales (
            transaction_id INTEGER PRIMARY KEY,
            customer_id TEXT,
            product_id TEXT,
            quantity INTEGER,
            sale_date DATE
        )
        """))


def get_last_transaction_id():
    with engine.connect() as conn:
        result = conn.execute(
            text(f"SELECT MAX({INCREMENTAL_KEY}) FROM {TABLE}")
        )
        return result.scalar() or 0


def insert_batch(df_batch):
    df_batch.to_sql(
        "sales",
        engine,
        if_exists="append",
        index=False
    )


def load_data_concurrent(df, max_workers=4):
    last_id = get_last_transaction_id()
    df = df[df["transaction_id"] > last_id]

    if df.empty:
        return 0

    total_rows = len(df)
    batches = [
        df.iloc[i:i + BATCH_SIZE]
        for i in range(0, total_rows, BATCH_SIZE)
    ]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(insert_batch, batches)

    return total_rows
