from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import customers as controller
from ..schemas import customers as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Customers'],
    prefix="/customers"
)

@router.post("/")
def create_customer(request: schema.CustomerCreate, db: Session = Depends(get_db)):
    return controller.create_customer(db=db, request=request)