from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Union
from app import models, schemas
from app.utils import generate_short_uuid, get_current_datetime


def get_period(db: Session):
    return db.query(models.Period).all()


def get_period_detail(db: Session, period_id=None):
    query = db.query(models.Checklist).join(models.Period).join(models.Member)

    if period_id is not None:
        query = query.filter(models.Period.id == period_id)
    else:
        # Subquery untuk mendapatkan tanggal `created_at` terbaru
        subquery = (
            db.query(func.max(models.Period.created_at))
            .scalar_subquery()
        )
        query = query.filter(models.Period.created_at == subquery)

    results = query.all()

    if not results:
        return results

    data = []
    for result in results:
        member = schemas.Member(id=result.member.id, name=result.member.name)
        number_status = [
            schemas.NumberStatus(number=juz, status=checklist)
            for juz, checklist in zip(result.juz, result.checklist)
        ]
        juz_status = schemas.JuzDetail(juz=number_status)
        data.append([member, juz_status])

    period_detail = schemas.PeriodDetail(
        can_update=results[0].period.can_update,
        can_lock=results[0].period.can_lock,
        is_done=results[0].period.is_done,
        period=results[0].period.id,
        data=data,
    )

    return period_detail


def create_period(db: Session, period: schemas.PeriodCreate):
    db_period = models.Period(id=generate_short_uuid(), name=period.name, created_at=get_current_datetime())
    db.add(db_period)
    db.commit()
    db.refresh(db_period)

    for member, juzs in period.data:
        db_checklist = models.Checklist(
            id=generate_short_uuid(),
            period_id=db_period.id,
            member_id=member[1],
            juz=juzs[1],
            checklist=[False] * len(juzs[1]),
            created_at=get_current_datetime(),
        )
        db.add(db_checklist)
        db.commit()
        db.refresh(db_checklist)
    return db_period


def update_period(
    db: Session,
    period_id: str,
    request: List[List[Union[schemas.Member, schemas.JuzDetail]]],
):
    completes = []
    for member, checklists in request.data:
        juzs = [juz.number for juz in checklists.juz]
        statuses = [checklist.status for checklist in checklists.juz]
        completes.append(True if all(status == True for status in statuses) else False)
        db_period = (
            db.query(models.Checklist)
            .filter(models.Checklist.member_id == member.id)
            .filter(models.Checklist.period_id == period_id)
            .first()
        )

        if not db_period:
            return None

        # db_period.juz = juzs
        db_period.checklist = statuses
        db_period.updated_at = get_current_datetime()
        db.commit()
        db.refresh(db_period)

    db_period = (
        db.query(models.Period).filter(models.Period.id == period_id).first()
    )
    db_period.can_lock = False
    if all(complete == True for complete in completes):
        db_period.can_lock = True
    db.commit()
    db.refresh(db_period)

    return get_period_detail(db, period_id)


def lock_period(db: Session, period_id: str):
    db_period = db.query(models.Period).filter(models.Period.id == period_id).first()
    db_period.is_done = True
    db_period.can_update = False
    db_period.can_lock = False
    db.commit()
    db.refresh(db_period)
    return get_period_detail(db, period_id)
