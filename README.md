# ETL-Data-Pipeline-Scenario
Full ETL process example scenario

## Generate mock data
python data\generate_mock_data.py

## Execute ETL
python main.py

## check DB output
import sqlite3
conn = sqlite3.connect("sales.db")
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM sales")
cursor.fetchone()