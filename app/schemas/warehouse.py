from datetime import datetime
from pydantic import BaseModel, ConfigDict


class WarehouseBase(BaseModel):
    name: str
    code: str
    location: str | None = None
    description: str | None = None
    is_active: bool = True


class WarehouseCreate(WarehouseBase):
    pass


class WarehouseUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    location: str | None = None
    description: str | None = None
    is_active: bool | None = None


class WarehouseResponse(WarehouseBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)