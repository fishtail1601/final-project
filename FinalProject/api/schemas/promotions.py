from datetime import date
from typing import Optional
from pydantic import BaseModel


class PromotionBase(BaseModel):
    order_id: Optional[int] = None
    menu_item_id: Optional[int] = None
    promotion_code: str
    expiration_date: date


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    order_id: Optional[int] = None
    menu_item_id: Optional[int] = None
    promotion_code: Optional[str] = None
    expiration_date: Optional[date] = None


class Promotion(PromotionBase):
    class ConfigDict:
        from_attributes = True