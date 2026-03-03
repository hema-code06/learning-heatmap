from fastapi import FastAPI
from .routers import auth, learning
from .database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv


app = FastAPI(title="Learning Analytics API")
load_dotenv()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(learning.router, prefix="/learning", tags=["Learning"])


@app.get("/")
def root():
    return {"message": "Learning Analytics API Running"}
