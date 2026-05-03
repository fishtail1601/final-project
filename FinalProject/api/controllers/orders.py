from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models.orders import Order
from ..models.order_details import OrderDetail
from ..models.customers import Customer
from ..models.promotions import Promotions
from ..models.recipes import Recipe
from ..models.resource_management import ResourceManagement
from ..schemas.orders import OrderCreate, GuestOrderCreate
from datetime import timedelta, datetime
from datetime import date

def check_ingredient_availability(db: Session, order_details: list):
    for detail in order_details:
        recipe_items = db.query(Recipe).filter(Recipe.sandwich_id == detail.sandwich_id).all()

        for item in recipe_items:
            resource = db.query(ResourceManagement).filter(ResourceManagement.resource_id == item.resource_id).first()

            total_needed = item.amount * detail.amount

            if not resource or resource.resource_amount < total_needed:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient ingredients: Not enough {resource.unit if resource else 'item'} to fulfill order."
                )
    return True

def apply_promo_code(db: Session, promo_code: str, order_price: float) -> tuple[float, Promotions]:
    if not promo_code:
        return order_price, None
    promo = db.query(Promotions).filter(Promotions.promotion_code == promo_code).first()
    if not promo:
        raise HTTPException(status_code=400, detail="Invalid promo code")
    if promo.expiration_date < date.today():
        raise HTTPException(status_code=400, detail="Promo code expired")
    if promo.discount_percentage:
        discount = order_price * (promo.discount_percentage / 100)
    elif promo.discount_amount:
        discount = promo.discount_amount
    else:
        discount = 0
    return max(0, order_price - discount), promo

def create_with_account(db: Session, request: OrderCreate):
    check_ingredient_availability(db, request.order_details)

    customer = db.query(Customer).filter(Customer.id == request.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Estimate time of order completion:
    prep_time = 8 + (len(request.order_details)) * 2
    estimate = datetime.now() + timedelta(minutes=prep_time)

    # Apply promo code if provided
    final_price, promo = apply_promo_code(db, request.promo_code, request.order_price)

    new_order = Order(
        customer_id=request.customer_id,
        description=request.description,
        order_status=request.order_status,
        order_type=request.order_type,
        order_price=final_price,
        tracking_number=request.tracking_number,
        ordered_time = datetime.now(),
        estimated_completion_time = estimate
    )

    # subtract ingredients in order from database:
    for detail in request.order_details:
        recipe_items = db.query(Recipe).filter(Recipe.sandwich_id == detail.sandwich_id).all()
        for item in recipe_items:
            resource = db.query(ResourceManagement).filter(ResourceManagement.resource_id == item.resource_id).first()
            resource.resource_amount -= (item.amount * detail.amount)

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in request.order_details:
        detail = OrderDetail(
            order_id=new_order.id,
            sandwich_id=item.sandwich_id,
            amount=item.amount
        )
        db.add(detail)

    # If promo was applied, link it to the order
    if promo:
        promo.order_id = new_order.id
        db.commit()

    db.commit()
    db.refresh(new_order)
    return new_order


def create_guest_order(db: Session, request: GuestOrderCreate):
    check_ingredient_availability(db, request.order_details)

    new_customer = Customer(
        customer_name=request.customer_name,
        customer_email=request.customer_email,
        customer_phone_number=request.customer_phone_number,
        customer_address=request.customer_address,
        hashed_password=""
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    # estimate time of order completion:

    prep_time = 8 + (len(request.order_details)) * 2
    estimate = datetime.now() + timedelta(minutes=prep_time)

    # Apply promo code if provided
    final_price, promo = apply_promo_code(db, request.promo_code, request.order_price)

    new_order = Order(
        customer_id=new_customer.id,
        description=request.description,
        order_status=request.order_status,
        order_type=request.order_type,
        order_price=final_price,
        tracking_number=request.tracking_number,
        ordered_time = datetime.now(),
        estimated_completion_time = estimate
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in request.order_details:
        detail = OrderDetail(
            order_id=new_order.id,
            sandwich_id=item.sandwich_id,
            amount=item.amount
        )
        db.add(detail)

    # If promo was applied, link it to the order
    if promo:
        promo.order_id = new_order.id
        db.commit()

    # subtract ingredients in order from database:
    for detail in request.order_details:
        recipe_items = db.query(Recipe).filter(Recipe.sandwich_id == detail.sandwich_id).all()
        for item in recipe_items:
            resource = db.query(ResourceManagement).filter(ResourceManagement.resource_id == item.resource_id).first()
            resource.resource_amount -= (item.amount * detail.amount)

    db.commit()
    db.refresh(new_order)
    return new_order


def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def complete_order(db: Session, order_id: int):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order:
        db_order.order_status = "Completed"
        db_order.actual_completion_time = datetime.now()
        db.commit()
        db.refresh(db_order)
    return db_order


def track_order(db: Session, tracking_num: str):
    item = db.query(model.Order).filter(model.Order.tracking_number == tracking_num).first()

    if not item:
        raise HTTPException(status_code=404, detail="Tracking number not found!")

    return item
