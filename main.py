from fastapi import FastAPI
from app.routes.storage import router as storage_router

app = FastAPI()

# Include Azure Blob Storage routes
app.include_router(storage_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
