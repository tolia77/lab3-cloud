from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.logging import init_sentry, setup_logging
from app.routers.football_router import router as football_router
from app.routers.favourite_router import router as favorites_router
from app.core.router import router as common_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_sentry()
    setup_logging()
    # # Initialize DB tables on startup
    # await _init_db_models()
    yield


app = FastAPI(
    title="Lab FastAPI Project",
    description="Lab project with FastAPI and Swagger UI",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(common_router)
app.include_router(football_router, prefix="/football")
app.include_router(favorites_router, prefix="/favorites")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
