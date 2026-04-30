from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..controllers import promotions as controller
from ..schemas.promotions import PromotionCreate, PromotionUpdate, Promotion

router = APIRouter(
    prefix="/promotions",
    tags=["Promotions"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=Promotion)
def create_promotion(promotion: PromotionCreate, db: Session = Depends(get_db)):
    return controller.create(db, promotion)

@router.get("/", response_model=list[Promotion])
def read_promotions(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{promo_code}", response_model=Promotion)
def read_promotion(promo_code: str, db: Session = Depends(get_db)):
    return controller.read_one(db, promo_code)

@router.put("/{promo_code}", response_model=Promotion)
def update_promotion(promo_code: str, promotion: PromotionUpdate, db: Session = Depends(get_db)):
    return controller.update(db, promo_code, promotion)

@router.delete("/{promo_code}")
def delete_promotion(promo_code: str, db: Session = Depends(get_db)):
    return controller.delete(db, promo_code)