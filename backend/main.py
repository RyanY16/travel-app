from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.get("/places")
def get_places():
    return [
        {
            "id": 1,
            "name": "Mt Takao",
            "category": "mountain",
            "lat": 35.625,
            "lon": 139.243
        },
        {
            "id": 2,
            "name": "Tokyo Skytree",
            "category": "landmark",
            "lat": 35.710,
            "lon": 139.810
        }
    ]
