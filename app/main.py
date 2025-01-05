from contextlib import asynccontextmanager
from app.system.database.connection import engine
from app.models import metadata
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.system.config import Config

from app.models import metadata
from app.system.database.connection import engine

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

app = FastAPI(
    title=Config.PROJECT_NAME,
)



@app.get("/", include_in_schema=False)
async def read_root():
    return RedirectResponse("/docs")

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
