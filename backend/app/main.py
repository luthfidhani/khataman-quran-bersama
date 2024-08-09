from fastapi import FastAPI
from app.routers import members, periods

app = FastAPI()

app.include_router(members.router, prefix="/member", tags=["members"])
app.include_router(periods.router, prefix="/period", tags=["periods"])


@app.get("/")
def root():
    return {"message": "Welcome to the Quran Khatam API"}
