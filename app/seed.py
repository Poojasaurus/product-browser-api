from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from datetime import datetime
import os
import uuid

from models import Product

load_dotenv("../.env")

DATABASE_URL = os.getenv("DATABASE_URL")

print("DATABASE_URL FOUND:", DATABASE_URL is not None)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

fake = Faker()

categories = [
    "electronics",
    "fashion",
    "books",
    "sports",
    "home",
    "toys"
]

session = SessionLocal()

BATCH_SIZE = 5000
TOTAL_PRODUCTS = 200000

try:

    for batch_start in range(0, TOTAL_PRODUCTS, BATCH_SIZE):

        products = []

        for _ in range(BATCH_SIZE):

            products.append(
                Product(
                    id=uuid.uuid4(),
                    name=fake.company(),
                    category=fake.random_element(categories),
                    price=round(fake.random_number(digits=4) / 10, 2),
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
            )

        session.bulk_save_objects(products)
        session.commit()

        print(f"Inserted {batch_start + BATCH_SIZE} products")

    print("Finished inserting 200000 products!")

except Exception as e:

    session.rollback()
    print("ERROR:", e)

finally:

    session.close()
