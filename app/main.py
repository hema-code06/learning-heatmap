from fastapi import FastAPI
from .routers import auth, learning
from .database import engine, Base
from . import models

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(learning.router, prefix="/learning", tags=["Learning"])


@app.get("/")
def root():
    return {"message": "Learning Heatmap API Running"}
