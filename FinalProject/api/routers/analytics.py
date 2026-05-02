from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from ..controllers import analytics as controller
from ..dependencies.database import get_db
from ..schemas import orders as order_schema
from ..schemas import ratings as rating_schema
from typing import List

router = APIRouter(
    tags=["Analytics"],
    prefix="/analytics"
)


@router.get("/revenue/daily")
def daily_revenue(target_date: date, db: Session = Depends(get_db)):
    return controller.get_daily_revenue(db, target_date)


@router.get("/orders/range", response_model=List[order_schema.Order])
def orders_by_date_range(start_date: date, end_date: date, db: Session = Depends(get_db)):
    return controller.get_orders_by_date_range(db, start_date, end_date)


@router.get("/sandwiches/popularity")
def sandwich_popularity(db: Session = Depends(get_db)):
    return controller.get_sandwich_popularity(db)


@router.get("/reviews/negative", response_model=List[rating_schema.Rating])
def negative_reviews(threshold: float = 3.0, db: Session = Depends(get_db)):
    return controller.get_negative_reviews(db, threshold)