from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from datetime import date
from ..models.orders import Order
from ..models.order_details import OrderDetail
from ..models.sandwiches import Sandwich
from ..models.ratings import Rating


def get_daily_revenue(db: Session, target_date: date):
    try:
        total = db.query(func.sum(Order.order_price)) \
            .filter(func.date(Order.order_date) == target_date) \
            .filter(Order.order_status != "cancelled") \
            .scalar()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"date": str(target_date), "total_revenue": float(total or 0.0)}


def get_orders_by_date_range(db: Session, start_date: date, end_date: date):
    if end_date < start_date:
        raise HTTPException(status_code=400, detail="end_date must be after start_date")
    try:
        orders = db.query(Order).filter(
            and_(
                func.date(Order.order_date) >= start_date,
                func.date(Order.order_date) <= end_date
            )
        ).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return orders


def get_sandwich_popularity(db: Session):
    try:
        results = db.query(
            Sandwich.id,
            Sandwich.sandwich_name,
            func.coalesce(func.sum(OrderDetail.amount), 0).label("times_ordered")
        ) \
            .outerjoin(OrderDetail, Sandwich.id == OrderDetail.sandwich_id) \
            .group_by(Sandwich.id, Sandwich.sandwich_name) \
            .order_by(func.coalesce(func.sum(OrderDetail.amount), 0).asc()) \
            .all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return [
        {"id": r.id, "sandwich_name": r.sandwich_name, "times_ordered": int(r.times_ordered)}
        for r in results
    ]


def get_negative_reviews(db: Session, threshold: float = 3.0):
    try:
        reviews = db.query(Rating) \
            .filter(Rating.rating <= threshold) \
            .order_by(Rating.rating.asc()) \
            .all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return reviews