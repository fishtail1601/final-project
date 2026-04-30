from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from ..models.promotions import Promotions
from ..schemas.promotions import PromotionCreate, PromotionUpdate, Promotion

def create(db: Session, request: PromotionCreate):
    try:
        new_promo = Promotions(
            promotion_code=request.promotion_code,
            discount_percentage=request.discount_percentage,
            discount_amount=request.discount_amount,
            expiration_date=request.expiration_date
        )
        db.add(new_promo)
        db.commit()
        db.refresh(new_promo)
        return new_promo
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

def read_all(db: Session):
    try:
        result = db.query(Promotions).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def read_one(db: Session, promo_code: str):
    try:
        item = db.query(Promotions).filter(Promotions.promotion_code == promo_code).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promo code not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

def update(db: Session, promo_code: str, request: PromotionUpdate):
    try:
        item = db.query(Promotions).filter(Promotions.promotion_code == promo_code).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promo code not found!")

        update_data = request.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)

        db.commit()
        db.refresh(item)
        return item
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

def delete(db: Session, promo_code: str):
    try:
        item = db.query(Promotions).filter(Promotions.promotion_code == promo_code).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promo code not found!")

        db.delete(item)
        db.commit()
        return {"message": "Promo code deleted successfully"}
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)