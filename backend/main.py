from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Literal, List

from sqlmodel import Session, select

from db import create_db_and_tables, get_session, engine
from models import Place, Visit

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

VisitStatus = Literal["not_visited", "visited", "explored"]


class VisitUpdate(BaseModel):
    place_id: int
    status: VisitStatus


# Optional: allow adding places later via API
class PlaceCreate(BaseModel):
    name: str
    category: str
    lat: float
    lon: float


def seed_places_if_empty(session: Session):
    existing = session.exec(select(Place)).first()
    if existing:
        return  # already seeded

    seed = [
        Place(name="Mt Takao", category="mountain", lat=35.625, lon=139.243),
        Place(name="Tokyo Skytree", category="landmark", lat=35.710, lon=139.810),
    ]
    session.add_all(seed)
    session.commit()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    # seed data once
    with Session(engine) as session:  # uses same engine as db.py
        seed_places_if_empty(session)


@app.get("/")
def root():
    return {"message": "Hello from the backend"}


@app.get("/places")
def get_places(session: Session = Depends(get_session)) -> List[dict]:
    places = session.exec(select(Place)).all()
    visits = session.exec(select(Visit)).all()
    status_by_place_id: Dict[int, str] = {v.place_id: v.status for v in visits}

    out = []
    for p in places:
        status = status_by_place_id.get(p.id, "not_visited")
        out.append(
            {
                "id": p.id,
                "name": p.name,
                "category": p.category,
                "lat": p.lat,
                "lon": p.lon,
                "status": status,
            }
        )
    return out


@app.post("/visits")
def set_visit(data: VisitUpdate, session: Session = Depends(get_session)):
    place = session.get(Place, data.place_id)
    if not place:
        return {"ok": False, "error": "Place not found"}

    existing = session.exec(select(Visit).where(Visit.place_id == data.place_id)).first()
    if existing:
        existing.status = data.status
    else:
        session.add(Visit(place_id=data.place_id, status=data.status))

    session.commit()
    return {"ok": True, "place_id": data.place_id, "status": data.status}


@app.post("/places")
def create_place(data: PlaceCreate, session: Session = Depends(get_session)):
    place = Place(name=data.name, category=data.category, lat=data.lat, lon=data.lon)
    session.add(place)
    session.commit()
    session.refresh(place)
    return {"ok": True, "id": place.id}
