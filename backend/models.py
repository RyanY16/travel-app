from typing import Optional, Literal
from sqlmodel import SQLModel, Field

VisitStatus = Literal["not_visited", "visited", "explored"]

class Place(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category: str
    lat: float
    lon: float

    country: str
    city: Optional[str] = None
    description: Optional[str] = None


class Visit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    place_id: int = Field(index=True, unique=True)
    status: str
