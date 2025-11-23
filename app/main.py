from fastapi import FastAPI
from alembic.config import Config
from alembic import command
import os

from app.routers.football_router import router as football_router
from app.routers.favourite_router import router as favorites_router

app = FastAPI(title="Football API Proxy with DB")

# Підключаємо роутери
app.include_router(football_router, prefix="/football")
app.include_router(favorites_router, prefix="/favorites")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# Функція для запуску міграцій на Render
def run_migrations():
    # Перевіряємо, чи існує файл alembic.ini (щоб не падало в тестах або якщо не налаштовано)
    if os.path.exists("alembic.ini"):
        alembic_cfg = Config("alembic.ini")
        try:
            command.upgrade(alembic_cfg, "head")
            print("Migrations applied successfully.")
        except Exception as e:
            print(f"Error applying migrations: {e}")

# Запускаємо міграції при старті (важливо для Render)
run_migrations()