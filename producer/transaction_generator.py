from faker import Faker
import random
from datetime import datetime, UTC
import json

fake = Faker()

transaction = {
    "transaction_id": fake.uuid4(),
    "user_id": random.randint(1000, 9999),
    "amount": round(random.uniform(100, 200000), 2),
    "merchant": fake.company(),
    "country": fake.country(),
    "timestamp": str(datetime.now(UTC))
}

print(json.dumps(transaction, indent=2))