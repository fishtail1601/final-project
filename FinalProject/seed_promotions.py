from datetime import date, timedelta
from sqlalchemy.orm import sessionmaker
from api.dependencies.database import engine
from api.models.promotions import Promotions

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Sample promo codes
promo_codes = [
    {
        "promotion_code": "WELCOME10",
        "discount_percentage": 10.00,
        "expiration_date": date.today() + timedelta(days=30)
    },
    {
        "promotion_code": "SAVE5",
        "discount_amount": 5.00,
        "expiration_date": date.today() + timedelta(days=60)
    },
    {
        "promotion_code": "HALFOFF",
        "discount_percentage": 50.00,
        "expiration_date": date.today() + timedelta(days=7)
    }
]

for promo_data in promo_codes:
    promo = Promotions(**promo_data)
    db.add(promo)

db.commit()
db.close()

print("Promo codes added to database")