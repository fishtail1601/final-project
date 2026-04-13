from typing import Optional
from pydantic import BaseModel


class MenuItemBase(BaseModel):
    dish_name: str
    dish_ingredients: str
    dish_price: float
    dish_calories: int
    dish_category: str


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    dish_name: Optional[str] = None
    dish_ingredients: Optional[str] = None
    dish_price: Optional[float] = None
    dish_calories: Optional[int] = None
    dish_category: Optional[str] = None


class MenuItem(MenuItemBase):
    id: int

    class ConfigDict:
        from_attributes = True