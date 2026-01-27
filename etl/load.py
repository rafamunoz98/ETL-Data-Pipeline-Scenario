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

def load_data(df):
    df.to_sql("sales", engine, if_exists="append", index=False)
