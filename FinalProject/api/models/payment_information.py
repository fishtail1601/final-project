from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, BOOLEAN
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class PaymentInformation(Base):
    __tablename__ = 'payment_information'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    card_information = Column(String(100))
    payment_type = Column(String(100))
    transaction_status = Column(BOOLEAN)

    customer = relationship("Customer", back_populates="payment_information")