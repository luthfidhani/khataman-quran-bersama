from fastapi import FastAPI
from app.routers import members, periods
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(members.router, prefix="/member", tags=["members"])
app.include_router(periods.router, prefix="/period", tags=["periods"])


@app.get("/")
def root():
    return {"message": "Welcome to the Quran Khatam API"}
