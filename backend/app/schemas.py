from typing import List, Union
from pydantic import BaseModel


class MemberBase(BaseModel):
    name: str


class MemberCreate(MemberBase):
    pass


class MemberDelete(BaseModel):
    id: str
    is_delete: bool = True


class MemberUpdate(BaseModel):
    id: str
    update: MemberBase


class Member(MemberBase):
    id: str

    class Config:
        orm_mode = True


class PeriodBase(BaseModel):
    name: str


class JuzList(BaseModel):
    id: str
    juz: List[int]


class PeriodCreate(PeriodBase):
    name: str
    data: List[JuzList]


class PeriodUpdate(BaseModel):
    id: str
    can_update: bool = False
    can_lock: bool = False
    is_done: bool = False


class Period(PeriodBase):
    id: str


class NumberStatus(BaseModel):
    number: int
    status: bool


class JuzDetail(BaseModel):
    juz: List[NumberStatus]


class UpdatePeriodRequest(BaseModel):
    data: List[List[Union[Member, JuzDetail]]]


class PeriodDetail(UpdatePeriodRequest):
    can_update: bool
    can_lock: bool
    is_done: bool
    period: str = "current"
