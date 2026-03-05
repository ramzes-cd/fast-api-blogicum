from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src import schemas, crud
from database import get_db

router = APIRouter(prefix="/locations", tags=["locations"])


# Создать локацию
@router.post("/", response_model=schemas.locations.LocationOut)
def create_location(
    location: schemas.locations.LocationCreate,
    db: Session = Depends(get_db)
):
    return crud.create_location(db=db, location=location)


# Получить все локации
@router.get("/", response_model=List[schemas.locations.LocationOut])
def read_locations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_locations(db, skip=skip, limit=limit)


# Получить одну локацию по ID
@router.get("/{location_id}", response_model=schemas.locations.LocationOut)
def read_location(
    location_id: int,
    db: Session = Depends(get_db)
):
    db_location = crud.get_location(db, location_id=location_id)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location


# Обновить локацию
@router.put("/{location_id}", response_model=schemas.locations.LocationOut)
def update_location(
    location_id: int,
    location: schemas.locations.LocationUpdate,
    db: Session = Depends(get_db)
):
    db_location = crud.update_location(db, location_id=location_id, location_update=location)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location


# Удалить локацию
@router.delete("/{location_id}", response_model=schemas.locations.LocationOut)
def delete_location(
    location_id: int,
    db: Session = Depends(get_db)
):
    db_location = crud.delete_location(db, location_id=location_id)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location