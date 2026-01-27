import yaml
import logging
from etl.extract import extract_csv
from etl.transform import transform_data
from etl.load import init_db, load_data

logging.basicConfig(
    filename="logs/etl.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("ETL process started")

with open("config/config.yaml") as f:
    config = yaml.safe_load(f)

init_db()

for chunk in extract_csv(
    config["paths"]["input_csv"],
    config["etl"]["chunk_size"]
):
    try:
        clean_df = transform_data(chunk)
        load_data(clean_df)
        logging.info(f"Loaded {len(clean_df)} records")
    except Exception as e:
        logging.error(f"Error processing chunk: {e}")

logging.info("ETL process completed successfully")
print("ETL completed successfully")
