from typing import Optional, Literal
from sqlmodel import SQLModel, Field

VisitStatus = Literal["not_visited", "visited", "explored"]


class Place(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category: str
    lat: float
    lon: float


class Visit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # single-user for now: one status per place
    place_id: int = Field(index=True, unique=True)

    status: str
