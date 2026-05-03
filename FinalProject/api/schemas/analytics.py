from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AnalyticsOrder(BaseModel):
    id: int
    customer_id: Optional[int] = None
    order_date: Optional[datetime] = None
    description: Optional[str] = None
    order_status: Optional[str] = None
    order_price: Optional[float] = None
    ordered_time: Optional[datetime] = None
    estimated_completion_time: Optional[datetime] = None
    actual_completion_time: Optional[datetime] = None


class AnalyticsCustomer(BaseModel):
    id: int
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone_number: Optional[str] = None
    customer_address: Optional[str] = None


class AnalyticsReview(BaseModel):
    id: int
    customer_id: Optional[int] = None
    text: Optional[str] = None
    rating: Optional[float] = None


class CustomerAnalytics(AnalyticsCustomer):
    orders: list[AnalyticsOrder] = Field(default_factory=list)
    reviews: list[AnalyticsReview] = Field(default_factory=list)


class AnalyticsData(BaseModel):
    orders: list[AnalyticsOrder] = Field(default_factory=list)
    customers: list[CustomerAnalytics] = Field(default_factory=list)
    reviews: list[AnalyticsReview] = Field(default_factory=list)
