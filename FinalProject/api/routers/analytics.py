from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from ..controllers import analytics as controller
from ..dependencies.database import get_db
from ..schemas import orders as order_schema
from ..schemas import ratings as rating_schema
from ..schemas import analytics as analytics_schema
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


@router.get("/orders", response_model=List[analytics_schema.AnalyticsOrder])
def all_order_data(db: Session = Depends(get_db)):
    return controller.get_all_order_data(db)


@router.get("/customers", response_model=List[analytics_schema.CustomerAnalytics])
def customer_analytics(db: Session = Depends(get_db)):
    return controller.get_customer_analytics(db)


@router.get("/sandwiches/popularity")
def sandwich_popularity(db: Session = Depends(get_db)):
    return controller.get_sandwich_popularity(db)


@router.get("/reviews", response_model=List[analytics_schema.AnalyticsReview])
def all_review_data(db: Session = Depends(get_db)):
    return controller.get_all_review_data(db)


@router.get("/reviews/negative", response_model=List[rating_schema.Rating])
def negative_reviews(threshold: float = 3.0, db: Session = Depends(get_db)):
    return controller.get_negative_reviews(db, threshold)


@router.get("/data", response_model=analytics_schema.AnalyticsData)
def analytics_data(db: Session = Depends(get_db)):
    return controller.get_analytics_data(db)
