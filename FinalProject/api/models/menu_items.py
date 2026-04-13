from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, BOOLEAN
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class MenuItems(Base):
    __tablename__ = 'menu_items'

    id = Column(Integer, primary_key=True)
    dish_name = Column(String(100))
    dish_ingredients = Column(String(100))
    dish_price = Column(DECIMAL(10, 2))
    dish_calories = Column(Integer)
    dish_category = Column(String(100))

    resource_management = relationship("ResourceManager", back_populates="menu_items")
