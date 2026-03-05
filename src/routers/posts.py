from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src import schemas, crud
from database import get_db

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=schemas.posts.PostOut, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.posts.PostCreate, db: Session = Depends(get_db)):
    author_id = post.author_id or 1
    return crud.create_post(db=db, post=post, author_id=author_id)


@router.get("/", response_model=List[schemas.posts.PostOut])
def read_posts(
    skip: int = 0,
    limit: int = 100,
    published_only: bool = True,
    db: Session = Depends(get_db)
):
    posts = crud.get_posts(db, skip=skip, limit=limit, published_only=published_only)
    return posts


@router.get("/{post_id}", response_model=schemas.posts.PostDetail)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.put("/{post_id}", response_model=schemas.posts.PostOut)
def update_post(post_id: int, post: schemas.posts.PostUpdate, db: Session = Depends(get_db)):
    db_post = crud.update_post(db, post_id=post_id, post_update=post)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.delete("/{post_id}", response_model=schemas.posts.PostOut)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.delete_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.get("/{post_id}/comments", response_model=List[schemas.comments.CommentOut])
def read_post_comments(post_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = crud.get_comments_by_post(db, post_id=post_id, skip=skip, limit=limit)
    return comments