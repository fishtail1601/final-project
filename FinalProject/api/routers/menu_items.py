from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..controllers import menu_items as controller
from ..dependencies.database import get_db
from ..schemas import menu_items as schema

router = APIRouter(
    tags=["Menu Items"],
    prefix="/menu",
)


@router.post("/", response_model=schema.MenuItem)
def create_menu_item(request: schema.MenuItemCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.MenuItem])
def read_menu_items(db: Session = Depends(get_db)):
    return controller.read_all(db=db)


@router.get("/{item_id}", response_model=schema.MenuItem)
def read_menu_item(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db=db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.MenuItem)
def update_menu_item(item_id: int, request: schema.MenuItemUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, item_id=item_id, request=request)


@router.delete("/{item_id}")
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)
