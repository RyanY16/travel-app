from fastapi import FastAPI

app = FastAPI()

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
