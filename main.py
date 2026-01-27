import yaml
from etl.extract import extract_csv
from etl.transform import transform_data
from etl.load import init_db, load_data

with open("config/config.yaml") as f:
    config = yaml.safe_load(f)

init_db()

for chunk in extract_csv(
    config["paths"]["input_csv"],
    config["etl"]["chunk_size"]
):
    clean_df = transform_data(chunk)
    load_data(clean_df)

print("ETL completed successfully")
