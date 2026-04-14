from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src import schemas, crud
from database import get_db

router = APIRouter(prefix="/users", tags=["users"])


# Удаление пользователя все посты и комментарии пользователя также будут удалены!
@router.delete("/{user_id}", response_model=schemas.users.UserOut)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return db_user


@router.post("/", response_model=schemas.users.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.users.UserCreate, db: Session = Depends(get_db)):
    db_user_by_nickname = crud.get_user_by_nickname(db, nickname=user.nickname)
    if db_user_by_nickname:
        raise HTTPException(status_code=400, detail="Nickname already registered")

    db_user_by_email = crud.get_user_by_email(db, email=user.email)
    if db_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(db=db, user=user)


@router.get("/", response_model=List[schemas.users.UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.users.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=schemas.users.UserOut)
def update_user(user_id: int, user: schemas.users.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id=user_id, user_update=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/{user_id}/posts", response_model=List[schemas.posts.PostOut])
def read_user_posts(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    all_posts = crud.get_posts(db, skip=skip, limit=limit, published_only=False)
    user_posts = [post for post in all_posts if post.author_id == user_id]
    return user_posts