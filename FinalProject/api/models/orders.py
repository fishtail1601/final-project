from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, BOOLEAN
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100))
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    description = Column(String(300))
    order_status = BOOLEAN
    order_price = Column(DECIMAL(10, 2))
    tracking_number = Column(Integer)

    order_details = relationship("OrderDetail", back_populates="order")
    promotions = relationship("Promotion", back_populates="order")