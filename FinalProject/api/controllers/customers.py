# controllers/customers.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models.customers import Customer
from ..schemas.customers import CustomerCreate

def create_customer(db: Session, request: CustomerCreate):
    existing_customer = db.query(Customer).filter(
        Customer.customer_email == request.customer_email
    ).first()

    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer email already registered"
        )

    new_customer = Customer(
        customer_name=request.customer_name,
        customer_email=request.customer_email,
        customer_phone_number=request.customer_phone_number,
        customer_address=request.customer_address,
        password=request.password
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer