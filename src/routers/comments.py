from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src import schemas, crud
from database import get_db

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/", response_model=schemas.comments.CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(comment: schemas.comments.CommentCreate, db: Session = Depends(get_db)):
    # Проверяем существование поста
    db_post = crud.get_post(db, post_id=comment.post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    # author_id должен браться из текущего авторизованного пользователя
    author_id = 1
    return crud.create_comment(db=db, comment=comment, author_id=author_id)


@router.put("/{comment_id}", response_model=schemas.comments.CommentOut)
def update_comment(comment_id: int, comment: schemas.comments.CommentUpdate, db: Session = Depends(get_db)):
    db_comment = crud.update_comment(db, comment_id=comment_id, comment_update=comment)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


@router.delete("/{comment_id}", response_model=schemas.comments.CommentOut)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = crud.delete_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment