from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, model_validator
from decimal import Decimal


class PromotionBase(BaseModel):
    order_id: Optional[int] = None
    menu_item_id: Optional[int] = None
    promotion_code: str
    discount_percentage: Optional[Decimal] = Field(
        default=None,
        ge=0,
        le=100,
        decimal_places=2,
        description="Discount as a percentage (0.00–100.00)"
    )
    discount_amount: Optional[Decimal] = Field(      # ← added here
        default=None,
        ge=0,
        description="Fixed discount amount in currency"
    )
    expiration_date: date

    @model_validator(mode="after")                   # ← moved here too
    def check_only_one_discount(self):
        if self.discount_percentage is not None and self.discount_amount is not None:
            raise ValueError("Only one of discount_percentage or discount_amount can be set.")
        return self


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(PromotionBase):                # ← now inherits from PromotionBase
    order_id: Optional[int] = None
    menu_item_id: Optional[int] = None
    promotion_code: Optional[str] = None
    expiration_date: Optional[date] = None


class Promotion(PromotionBase):
    id: int

    class Config:
        from_attributes = True