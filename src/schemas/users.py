from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    bio_info: str | None = None
    email: EmailStr | None = None


class UserCreate(UserBase):
    nickname: str
    password: str


class UserUpdate(UserBase):
    pass


class UserOut(UserBase):
    id: int
    nickname: str
    active: bool
    date_joined: datetime

    class Config:
        from_attributes = True