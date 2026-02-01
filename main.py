import yaml
import logging
from etl.extract import extract_csv
from etl.transform import transform_data
from etl.load import init_db, load_data_concurrent

# Configure basic logging for the ETL run
logging.basicConfig(
    filename="logs/etl.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("ETL process started")

# Load pipeline configuration (paths, ETL settings, etc.)
with open("config/config.yaml") as f:
    config = yaml.safe_load(f)

# Ensure the target database/table exists before loading data
init_db()


def main():
    """
    Orchestrates the full ETL pipeline: extract CSV chunks, transform each
    chunk according to data quality and schema rules, and load the results
    into the target database using concurrent batch inserts.

    The function reads settings from `config/config.yaml` for input paths
    and ETL parameters like `chunk_size` and `max_workers`.
    """
    
    error_count = 0
    
    # Iterate over CSV chunks: pandas returns an iterator that maintains an internal
    # file pointer, so each iteration reads the next chunk without repeating or skipping rows
    for chunk in extract_csv(
        config["paths"]["input_csv"],
        config["etl"]["chunk_size"]
    ):
        try:
            # Apply transformations and data quality rules
            clean_df = transform_data(chunk)

            # Load transformed data into the database concurrently
            rows = load_data_concurrent(
                clean_df,
                config["etl"]["max_workers"]
            )

            logging.info(f"Loaded {rows} records")
        except Exception as e:
            # Log errors per chunk but continue processing remaining chunks
            logging.error(f"Error processing chunk: {e}")
            error_count += 1

    if error_count > 0:
        logging.warning(f"ETL process completed with {error_count} errors")
        print("ETL completed with errors")
    else:
        logging.info("ETL process completed successfully")
        print("ETL completed successfully")


if __name__ == "__main__":
    main()
