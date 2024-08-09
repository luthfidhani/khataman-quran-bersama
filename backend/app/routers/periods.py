from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app import schemas
from app.cruds import period as crud
from sqlalchemy.orm import Session
from app.deps import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Period], status_code=status.HTTP_200_OK)
def get_periods(db: Session = Depends(get_db)):
    return crud.get_period(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_period(request: schemas.PeriodCreate, db: Session = Depends(get_db)):
    crud.create_period(db, request)
    return {"status": "success"}


@router.get(
    "/current", response_model=schemas.PeriodDetail, status_code=status.HTTP_200_OK
)
def get_current_period(db: Session = Depends(get_db)):
    return crud.get_period_detail(db)


@router.get(
    "/{period_id}", response_model=schemas.PeriodDetail, status_code=status.HTTP_200_OK
)
def get_period_by_id(period_id: str, db: Session = Depends(get_db)):
    result = crud.get_period_detail(db, period_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Period not found"
        )
    return result


@router.put(
    "/{period_id}", response_model=schemas.PeriodDetail, status_code=status.HTTP_200_OK
)
def update_period(
    period_id: str, request: schemas.UpdatePeriodRequest, db: Session = Depends(get_db)
):
    result = crud.update_period(db, period_id, request)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Period not found"
        )
    return result


@router.post("/{period_id}/lock", status_code=status.HTTP_200_OK)
def lock_period(period_id: str, db: Session = Depends(get_db)):
    result = crud.lock_period(db, period_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Period not found"
        )
    return result
