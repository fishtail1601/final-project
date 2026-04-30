from datetime import date
from typing import Optional
from pydantic import BaseModel
from decimal import Decimal


class PromotionBase(BaseModel):
    order_id: Optional[int] = None
    menu_item_id: Optional[int] = None
    promotion_code: str
    discount_percentage: Optional[Decimal] = None
    expiration_date: date


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    order_id: Optional[int] = None
    menu_item_id: Optional[int] = None
    promotion_code: Optional[str] = None
    discount_percentage: Optional[Decimal] = None
    discount_amount: Optional[Decimal] = None
    expiration_date: Optional[date] = None


class Promotion(PromotionBase):
    id: int

    class Config:
        from_attributes = True