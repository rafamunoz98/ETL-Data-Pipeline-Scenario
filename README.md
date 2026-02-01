# ETL Data Pipeline – Allianz Data Engineer Challenge

## Overview

This project implements a **production‑ready ETL (Extract, Transform, Load) pipeline in Python**. The pipeline ingests sales transaction data from a CSV file, applies data quality checks and transformations, encrypts sensitive information, and loads the data **incrementally and concurrently** into a SQL database. It is also designed to handle large datasets efficiently by processing data in chunks and avoiding full in-memory loads.

The solution is designed to be **scalable, secure, and maintainable**, following data engineering best practices.

---

## Architecture

```
ETL-Data-Pipeline-Scenario/
├── data/
│   ├── sales.csv                  # Input CSV (mock data)
│   └── generate_mock_data.py      # Mock data generator
├── etl/
│   ├── extract.py                 # CSV extraction (chunked)
│   ├── transform.py               # Data cleaning, validation, encryption
│   ├── load.py                    # Incremental & concurrent loading
│   └── encryption.py              # AES (Fernet) encryption utilities
├── config/
│   ├── secrets.yaml               # External configuration (not versioned)
│   └── config.yaml                # External configuration (versioned, non-sensitive)
├── logs/
│   └── etl.log                    # Execution logs
├── main.py                        # ETL orchestration
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Features

* **Chunked extraction** for large datasets
* **Data quality checks** (nulls, invalid values, duplicates)
* **Schema transformation** and normalization
* **Encryption of sensitive fields** (`customer_id`, `product_id`)
* **Incremental loading** using a primary key watermark
* **Concurrent batch inserts** using `ThreadPoolExecutor`
* **Externalized configuration** via YAML
* **Robust logging and error handling**
* **Portable design** (SQLite for demo, PostgreSQL/MySQL ready)
* **Large dataset handling** via chunked processing and streaming

---

## Technologies Used

* Python 3.10+
* pandas
* SQLAlchemy
* SQLite (demo database)
* cryptography (Fernet / AES)
* PyYAML
* Faker

---

## Setup Instructions (Windows)

### 1. Create and activate virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Generate mock data

```powershell
python data\generate_mock_data.py
```

### 4. Configure the application

Edit `config/config.yaml` for non-sensitive settings (this file may be versioned):

```yaml
database:
  url: sqlite:///sales.db
  table: sales

paths:
  input_csv: data/sales.csv

etl:
  chunk_size: 5000
  max_workers: 4
```

---

## Secrets (do not commit)

Keep sensitive values in a separate `config/secrets.yaml` which is ignored by git. Example:

```yaml
security:
  encryption_key: "<FERNET_BASE64_KEY>"
```

Generate a Fernet key locally with Python and store it in `config/secrets.yaml`:

```powershell
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

---

## Running the ETL

```powershell
python main.py
```

Expected output:

```
ETL completed successfully
```

Artifacts generated:

* `sales.db` – SQLite database
* `logs/etl.log` – execution logs

---

## Viewing the SQLite database

You can inspect the loaded data using:

```python
import sqlite3

conn = sqlite3.connect("sales.db")
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM sales")
cursor.fetchone()
cursor.execute("""
SELECT *
FROM sales
LIMIT 5
""")
cursor.fetchall()

```

These commands let you quickly validate inserts and preview data after running the ETL.

To decode the output:

```powershell
python scripts/decrypt_sample.py
```

To delete the db
```powershell
Remove-Item sales.db
```

---

## Incremental Loading Strategy

* `transaction_id` is used as a **watermark**
* The pipeline queries `MAX(transaction_id)` from the target table
* Only new records are loaded on subsequent runs
* The incremental key should be indexed in production for optimal performance

This ensures **idempotency** and avoids duplicate data.

---

## Concurrency Model

* Data is split into fixed‑size batches
* Batches are loaded in parallel using `ThreadPoolExecutor`
* Each thread uses its own database connection

The concurrency model is limited by SQLite write locking, but scales linearly when used with PostgreSQL or MySQL.

---

## Security Considerations

* Sensitive identifiers are encrypted using **AES (Fernet)**
* Configuration files and secrets are excluded via `.gitignore`
* Designed to integrate with a secrets manager in production

---

## Schema Evolution Handling

* CSV columns are read dynamically
* Required fields are validated
* New or missing columns can be handled without data loss
* Logic can be extended with schema versioning

---

## Known Limitations

* SQLite limits concurrent writes and is used for demo purposes only
* Encryption is symmetric and intended for identifier protection, not PII storage
* Schema versioning can be extended for more complex evolution scenarios

---

## Version Control

* Git used for source control
* Clean commit history
* `.gitignore` excludes environments, secrets, logs, and local databases


---

## Author

Prepared as part of the **Allianz Data Engineer technical challenge**.
