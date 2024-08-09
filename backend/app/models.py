from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    TIMESTAMP,
    ForeignKey,
    ARRAY,
)
from sqlalchemy.orm import relationship
from .database import Base


class Member(Base):
    __tablename__ = "member"

    id = Column(
        String,
        primary_key=True,
        unique=True,
    )
    name = Column(String)
    created_at = Column(TIMESTAMP, default=None)
    updated_at = Column(TIMESTAMP, default=None)
    is_delete = Column(Boolean, default=False)

    checklists = relationship("Checklist", back_populates="member")


class Period(Base):
    __tablename__ = "period"

    id = Column(
        String,
        primary_key=True,
        unique=True,
    )
    name = Column(String)
    can_update = Column(Boolean, default=True)
    can_lock = Column(Boolean, default=False)
    is_done = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=None)
    updated_at = Column(TIMESTAMP, default=None)

    checklists = relationship("Checklist", back_populates="period")


class Checklist(Base):
    __tablename__ = "checklist"

    id = Column(
        String,
        primary_key=True,
        unique=True,
    )
    member_id = Column(Integer, ForeignKey("member.id"))
    period_id = Column(Integer, ForeignKey("period.id"))
    juz = Column(ARRAY(String))
    checklist = Column(ARRAY(Boolean))
    created_at = Column(TIMESTAMP, default=None)
    updated_at = Column(TIMESTAMP, default=None)

    member = relationship("Member", back_populates="checklists")
    period = relationship("Period", back_populates="checklists")
