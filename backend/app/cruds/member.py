from sqlalchemy.orm import Session
from app import models, schemas
from app.utils import generate_short_uuid, get_current_datetime


def get_member(db: Session):
    return db.query(models.Member).filter(models.Member.is_delete == False).all()


def create_member(db: Session, member: schemas.MemberCreate):
    db_member = models.Member(id=generate_short_uuid(), name=member.name, created_at=get_current_datetime())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def delete_member(db: Session, member: schemas.MemberDelete):
    db_member = db.query(models.Member).filter(models.Member.id == member.id).first()
    if db_member:
        db_member.is_delete = True
        db_member.updated_at = get_current_datetime()
        db.commit()
        db.refresh(db_member)
    return db_member


def update_member(db: Session, member: schemas.MemberUpdate):
    db_member = db.query(models.Member).filter(models.Member.id == member.id).first()
    if db_member:
        db_member.name = member.update.name
        db_member.updated_at = get_current_datetime()
        db.commit()
        db.refresh(db_member)
    return db_member
