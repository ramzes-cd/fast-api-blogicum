from pydantic import BaseModel, Field
from datetime import datetime


class LocationBase(BaseModel):
    name: str = None
    is_published: bool = None


class LocationCreate(LocationBase):
    name: str
    is_published: bool = False


class LocationUpdate(LocationBase):
    pass


class LocationOut(LocationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True