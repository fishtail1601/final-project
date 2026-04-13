from typing import Optional
from pydantic import BaseModel


class RatingBase(BaseModel):
    customer_id: int
    text: str
    rating: float


class RatingCreate(RatingBase):
    pass


class RatingUpdate(BaseModel):
    customer_id: Optional[int] = None
    text: Optional[str] = None
    rating: Optional[float] = None


class Rating(RatingBase):
    id: int

    class ConfigDict:
        from_attributes = True