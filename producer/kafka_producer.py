from kafka import KafkaProducer
from faker import Faker
from datetime import datetime, UTC
import json
import random
import time

fake = Faker()

producer = KafkaProducer(
    bootstrap_servers='localhost:29092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks='all',
    retries=3
)

def generate_transaction():
    return {
        "transaction_id": fake.uuid4(),
        "user_id": random.randint(1000, 9999),
        "amount": round(random.uniform(100, 200000), 2),
        "merchant": fake.company(),
        "country": fake.country(),
        "timestamp": str(datetime.now(UTC))
    }

while True:
    transaction = generate_transaction()

    producer.send("transactions", transaction)

    producer.flush()

    print(f"Sent: {transaction}")

    time.sleep(1)