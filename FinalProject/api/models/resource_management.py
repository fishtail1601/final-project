from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, BOOLEAN
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class ResourceManagement(Base):
    __tablename__ = 'resource_management'

    resource_id = Column(Integer, ForeignKey('menu_items.id'), primary_key=True)
    resource_amount = Column(Integer)

    menu_items = relationship("MenuItems", back_populates="resource_management")
