from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, BOOLEAN, Date
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Promotions(Base):
    __tablename__ = 'promotions'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=True)
    promotion_code = Column(String(100), unique=True)
    discount_percentage = Column(DECIMAL(5, 2), nullable=True)  # e.g., 10.00 for 10%
    discount_amount = Column(DECIMAL(10, 2), nullable=True)  # e.g., 5.00 for $5 off
    expiration_date = Column(Date)

    order = relationship("Order", back_populates="promotions")
    menu_item = relationship("MenuItems", back_populates="promotions")