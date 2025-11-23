from fastapi import FastAPI
from alembic.config import Config
from alembic import command
import os

from app.routers.football_router import router as football_router
from app.routers.favourite_router import router as favorites_router

app = FastAPI(title="Football API Proxy with DB")

app.include_router(football_router, prefix="/football")
app.include_router(favorites_router, prefix="/favorites")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
