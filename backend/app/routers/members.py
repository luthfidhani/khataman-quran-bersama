from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app import schemas
from app.cruds import member as crud
from sqlalchemy.orm import Session
from app.deps import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Member], status_code=status.HTTP_200_OK)
def get_members(db: Session = Depends(get_db)):
    return crud.get_members(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_member(request: schemas.MemberCreate, db: Session = Depends(get_db)):
    crud.create_member(db, request)
    return {"status": "success"}


@router.delete("/", status_code=status.HTTP_200_OK)
def delete_member(request: schemas.MemberDelete, db: Session = Depends(get_db)):
    db_user = crud.delete_member(db, request)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found"
        )
    return {"status": "success"}


@router.put("/", status_code=status.HTTP_200_OK)
def update_member(request: schemas.MemberUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_member(db, request)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Member not found"
        )
    return {"status": "success"}
