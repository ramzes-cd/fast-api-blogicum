from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from src.schemas.users import UserOut
from src.schemas.categories import CategoryOut
from src.schemas.locations import LocationOut
from src.schemas.comments import CommentOut


class PostBase(BaseModel):
    title: str | None = None
    text: str | None = None
    pub_date: datetime | None = None
    is_published: bool | None = None
    image: str | None = None
    location_id: int | None = None
    category_id: int | None = None


class PostCreate(PostBase):
    title: str
    text: str
    pub_date: datetime
    author_id: int | None = None  # Можно убрать, если будем брать из текущего пользователя


class PostUpdate(PostBase):
    pass


class PostOut(PostCreate):
    id: int
    created_at: datetime
    author_id: int

    class Config:
        from_attributes = True


class PostDetail(PostOut):
    author: UserOut
    category: Optional[CategoryOut] = None
    location: Optional[LocationOut] = None
    comments: List[CommentOut] = []

    class Config:
        from_attributes = True