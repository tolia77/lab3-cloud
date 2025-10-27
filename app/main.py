from fastapi import FastAPI
from app.routers.football_router import router as football_router

app = FastAPI(title="Football API Proxy")

# mount under /football (change prefix if desired)
app.include_router(football_router, prefix="/football")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
