from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail


class OrderItemCreate(BaseModel):
    sandwich_id: int
    amount: int


class OrderBase(BaseModel):
    customer_id: int
    description: Optional[str] = None
    order_status: Optional[str] = None
    order_price: Optional[float] = None
    tracking_number: Optional[str] = None


class OrderCreate(OrderBase):
    customer_id: int
    order_details: list[OrderItemCreate] = []
    promo_code: Optional[str] = None


class GuestOrderCreate(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone_number: Optional[str] = None
    customer_address: Optional[str] = None
    description: Optional[str] = None
    order_status: Optional[str] = None
    order_price: Optional[float] = None
    tracking_number: Optional[str] = None
    order_details: list[OrderItemCreate] = []
    promo_code: Optional[str] = None


class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    description: Optional[str] = None
    order_status: Optional[str] = None
    order_price: Optional[float] = None
    tracking_number: Optional[str] = None


class Order(OrderBase):
    id: int
    customer_id: Optional[int] = None
    order_date: Optional[datetime] = None
    order_details: list[OrderDetail] = []
    ordered_time: datetime
    estimated_completion_time: Optional[datetime]
    actual_completion_time: Optional[datetime]

    class ConfigDict:
        from_attributes = True
