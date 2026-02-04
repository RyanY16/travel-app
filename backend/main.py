from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Literal, List

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

PLACES = [
    {"id": 1, "name": "Mt Takao", "category": "mountain", "lat": 35.625, "lon": 139.243},
    {"id": 2, "name": "Tokyo Skytree", "category": "landmark", "lat": 35.710, "lon": 139.810},
]

VISITS: Dict[int, VisitStatus] = {}

class VisitUpdate(BaseModel):
    place_id: int
    status: VisitStatus

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.get("/places")
def get_places() -> List[dict]:
    # Attach the saved status to each place
    out = []
    for p in PLACES:
        status: VisitStatus = VISITS.get(p["id"], "not_visited")
        out.append({**p, "status": status})
    return out

@app.post("/visits")
def set_visit(data: VisitUpdate):
    # Validate place exists
    if not any(p["id"] == data.place_id for p in PLACES):
        return {"ok": False, "error": "Place not found"}

    VISITS[data.place_id] = data.status
    return {"ok": True, "place_id": data.place_id, "status": data.status}