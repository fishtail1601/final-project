from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, BOOLEAN
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    description = Column(String(300))
    order_status = Column(String(50))
    order_price = Column(DECIMAL(10, 2))
    tracking_number = Column(String(100))

    ordered_time = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    estimated_completion_time = Column(DATETIME, nullable=True)
    actual_completion_time = Column(DATETIME, nullable=True)

    order_details = relationship("OrderDetail", back_populates="order")
    promotions = relationship("Promotions", back_populates="order")
    customer = relationship("Customer", back_populates="orders")