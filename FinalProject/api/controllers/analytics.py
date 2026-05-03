from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from datetime import date
from ..models.orders import Order
from ..models.order_details import OrderDetail
from ..models.sandwiches import Sandwich
from ..models.ratings import Rating
from ..models.customers import Customer


def _order_data(order: Order):
    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "order_date": order.order_date,
        "description": order.description,
        "order_status": order.order_status,
        "order_price": float(order.order_price or 0),
        "tracking_number": order.tracking_number,
        "ordered_time": order.ordered_time,
        "estimated_completion_time": order.estimated_completion_time,
        "actual_completion_time": order.actual_completion_time,
    }


def _review_data(review: Rating):
    return {
        "id": review.id,
        "customer_id": review.customer_id,
        "text": review.text,
        "rating": float(review.rating or 0),
    }


def _customer_data(customer: Customer):
    return {
        "id": customer.id,
        "customer_name": customer.customer_name,
        "customer_email": customer.customer_email,
        "customer_phone_number": customer.customer_phone_number,
        "customer_address": customer.customer_address,
        "orders": [_order_data(order) for order in customer.orders],
        "reviews": [_review_data(review) for review in customer.ratings],
    }


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


def get_all_order_data(db: Session):
    try:
        orders = db.query(Order).order_by(Order.order_date.desc()).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return [_order_data(order) for order in orders]


def get_customer_analytics(db: Session):
    try:
        customers = db.query(Customer).order_by(Customer.id.asc()).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return [_customer_data(customer) for customer in customers]


def get_all_review_data(db: Session):
    try:
        reviews = db.query(Rating).order_by(Rating.id.desc()).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return [_review_data(review) for review in reviews]


def get_analytics_data(db: Session):
    return {
        "orders": get_all_order_data(db),
        "customers": get_customer_analytics(db),
        "reviews": get_all_review_data(db),
    }


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
