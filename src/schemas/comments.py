from pydantic import BaseModel
from datetime import datetime


class CommentBase(BaseModel):
    text: str | None = None


class CommentCreate(CommentBase):
    text: str
    post_id: int


class CommentUpdate(CommentBase):
    pass


class CommentOut(CommentCreate):
    id: int
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True