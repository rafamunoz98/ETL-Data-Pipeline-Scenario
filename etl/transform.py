import pandas as pd
from etl.encryption import get_cipher, encrypt_value
import yaml

# Load configuration file containing data quality rules and schema definitions
with open("config/config.yaml") as f:
    config = yaml.safe_load(f)

# Load secrets file containing sensitive information like encryption keys
with open("config/secrets.yaml") as f:
    secrets = yaml.safe_load(f)

# Initialize cipher object for encrypting sensitive data
cipher = get_cipher(secrets["security"]["encryption_key"])

# Load configuration values for data validation and transformation
REQUIRED_COLUMNS = config["data_quality"]["required_columns"]
ENCRYPTED_COLUMNS = config["security"]["encrypted_columns"]
MIN_QUANTITY = config["data_quality"]["quantity_min"]
OUTPUT_COLUMNS = list(config["schema"]["output_columns"].keys())

# Function to validate that all required columns are present in the dataframe
def validate_schema(df, required_columns):
    """
    Validates that the dataframe contains all required columns.
    
    Args:
        df (pd.DataFrame): The dataframe to validate
        required_columns (list): List of column names that must be present
        
    Raises:
        ValueError: If any required columns are missing
    """
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


# Main transformation function that applies data quality rules and encryption
def transform_data(df):
    """
    Applies data quality rules, validation, encryption, and formatting to the dataframe.
    
    Args:
        df (pd.DataFrame): The input dataframe to transform
        
    Returns:
        pd.DataFrame: The transformed dataframe with applied rules
    """
    # Schema validation (hard fail if required columns are missing)
    validate_schema(df, REQUIRED_COLUMNS)

    # Drop rows with missing values in required columns
    df = df.dropna(subset=REQUIRED_COLUMNS)

    # Apply data quality rules: filter rows where quantity is below minimum threshold
    df = df[df["quantity"] >= MIN_QUANTITY]

    # Encrypt sensitive columns to protect personal/confidential data
    # Only processes columns that exist in the dataframe
    for col in ENCRYPTED_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(str).apply(
                lambda x: encrypt_value(x, cipher)
            )

    # Convert timestamp column to sale_date (extract date only, remove time)
    df["sale_date"] = pd.to_datetime(df["timestamp"]).dt.date

    # Select only the expected output columns, excluding any extra columns in the dataframe
    df = df[[col for col in OUTPUT_COLUMNS if col in df.columns]]

    return df
