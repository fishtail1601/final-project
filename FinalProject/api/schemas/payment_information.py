from typing import Optional
from pydantic import BaseModel


class PaymentInformationBase(BaseModel):
    customer_id: int
    card_information: str
    payment_type: str
    transaction_status: bool


class PaymentInformationCreate(PaymentInformationBase):
    pass


class PaymentInformationUpdate(BaseModel):
    customer_id: Optional[int] = None
    card_information: Optional[str] = None
    payment_type: Optional[str] = None
    transaction_status: Optional[bool] = None


class PaymentInformation(PaymentInformationBase):
    id: int

    class ConfigDict:
        from_attributes = True