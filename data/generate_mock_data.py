import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

START_ID = 20000
NUM_RECORDS = 20000

data = []
start_date = datetime.now() - timedelta(days=30)

for i in range(START_ID, NUM_RECORDS + START_ID):
    data.append({
        "transaction_id": i,
        "customer_id": f"CUST_{random.randint(1, 500)}",
        "product_id": f"PROD_{random.randint(1, 100)}",
        "quantity": random.randint(1, 5),
        "timestamp": fake.date_time_between(start_date=start_date, end_date="now")
    })

df = pd.DataFrame(data)
df.to_csv("data/sales.csv", index=False)

print("Mock data generated: data/sales.csv")
