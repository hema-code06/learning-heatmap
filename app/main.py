from fastapi import FastAPI
from .routers import learning
from .database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv


app = FastAPI()
load_dotenv()

Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(learning.router, prefix="/learning", tags=["Learning"])


@app.get("/")
def root():
    return {"message": "Learning Analytics API Running"}
