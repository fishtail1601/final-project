from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, BOOLEAN, Date
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Promotions(Base):
    __tablename__ = 'promotions'

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=True)
    promotion_code = Column(String, primary_key=True)
    expiration_date = Column(Date)

    order = relationship("Order", back_populates="promotions")
    menu_item = relationship("MenuItems", back_populates="promotions")