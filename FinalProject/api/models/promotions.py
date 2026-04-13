from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, BOOLEAN, Date
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Promotions(Base):
    __tablename__ = 'promotions'

    promotion_code = Column(String, primary_key=True)
    expiration_date = Column(Date)

    order = relationship("Order", back_populates="promotions")