from typing import Optional
from pydantic import BaseModel


class ResourceManagementBase(BaseModel):
    resource_id: int
    resource_amount: int
    unit: Optional[str] = None


class ResourceManagementCreate(ResourceManagementBase):
    pass


class ResourceManagementUpdate(BaseModel):
    resource_id: Optional[int] = None
    resource_amount: Optional[int] = None
    unit: Optional[str] = None


class ResourceManagement(ResourceManagementBase):
    class ConfigDict:
        from_attributes = True