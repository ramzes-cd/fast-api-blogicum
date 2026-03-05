from pydantic import BaseModel
from datetime import datetime


class CategoryBase(BaseModel):
    slug: str = None
    title: str = None
    description: str = None
    is_published: bool = None


class CategoryCreate(CategoryBase):
    slug: str
    title: str
    description: str | None = None
    is_published: bool = False


class CategoryUpdate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True