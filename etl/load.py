from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///sales.db")

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
        result = conn.execute(text("SELECT MAX(transaction_id) FROM sales"))
        return result.scalar() or 0

def load_data(df):
    last_id = get_last_transaction_id()
    df = df[df["transaction_id"] > last_id]

    if not df.empty:
        df.to_sql("sales", engine, if_exists="append", index=False)
