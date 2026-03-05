from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src import schemas, crud
from database import get_db

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=schemas.categories.CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.categories.CategoryCreate, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_slug(db, slug=category.slug)
    if db_category:
        raise HTTPException(status_code=400, detail="Category with this slug already exists")
    return crud.create_category(db=db, category=category)


@router.get("/", response_model=List[schemas.categories.CategoryOut])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories


@router.get("/{category_id}", response_model=schemas.categories.CategoryOut)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.put("/{category_id}", response_model=schemas.categories.CategoryOut)
def update_category(category_id: int, category: schemas.categories.CategoryUpdate, db: Session = Depends(get_db)):
    db_category = crud.update_category(db, category_id=category_id, category_update=category)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.delete("/{category_id}", response_model=schemas.categories.CategoryOut)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.delete_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category