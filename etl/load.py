from sqlalchemy import create_engine, text
from concurrent.futures import ThreadPoolExecutor
import math
import yaml

# Load configuration file containing database and ETL settings
with open("config/config.yaml") as f:
    config = yaml.safe_load(f)

# Load configuration values for database operations
TABLE = config["database"]["table"]
BATCH_SIZE = config["etl"]["batch_size"]
INCREMENTAL_KEY = config["etl"]["incremental_key"]
DATABASE_PATH = config["database"]["url"]

# Create SQLAlchemy engine to connect to the SQLite database
engine = create_engine(
    DATABASE_PATH,
    connect_args={"check_same_thread": False}
)


# Function to initialize the database and create the sales table if it doesn't exist
def init_db():
    """
    Creates the sales table in the database with the required schema.
    Runs only if the table doesn't already exist.
    """
    with engine.connect() as conn:

        conn.execute(text(f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
            transaction_id INTEGER PRIMARY KEY,
            customer_id TEXT,
            product_id TEXT,
            quantity INTEGER,
            sale_date DATE
        )
        """))


# Function to get the last transaction ID from the database (for incremental loads)
def get_last_transaction_id():
    """
    Retrieves the maximum transaction_id currently in the database.
    Used to determine which records are new and should be inserted.
    
    Returns:
        int: The maximum transaction_id, or 0 if the table is empty
    """
    with engine.connect() as conn:
        result = conn.execute(
            text(f"SELECT MAX({INCREMENTAL_KEY}) FROM {TABLE}")
        )
        return result.scalar() or 0


# Function to insert a batch of records into the database
def insert_batch(df_batch):
    """
    Inserts a batch of records into the sales table.
    
    Args:
        df_batch (pd.DataFrame): The batch of records to insert
    """
    df_batch.to_sql(
        TABLE,
        engine,
        if_exists="append",
        index=False
    )


# Main function to load data using concurrent batch processing
def load_data_concurrent(df, max_workers=4):
    """
    Loads data into the database using concurrent processing for improved performance.
    Implements incremental load logic to skip records already in the database.
    
    Args:
        df (pd.DataFrame): The dataframe containing records to load
        max_workers (int): The maximum number of threads to use for concurrent processing
        
    Returns:
        int: The number of new records inserted
    """
    # Get the last transaction ID to identify new records
    last_id = get_last_transaction_id()
    df = df[df["transaction_id"] > last_id]

    # Return early if there are no new records to insert
    if df.empty:
        return 0

    # Split the dataframe into batches for concurrent processing
    total_rows = len(df)
    batches = [
        df.iloc[i:i + BATCH_SIZE]
        for i in range(0, total_rows, BATCH_SIZE)
    ]

    # Execute batch inserts concurrently using thread pool
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(insert_batch, batches)

    return total_rows
