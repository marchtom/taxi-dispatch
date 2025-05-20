import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import run_migrations


@asynccontextmanager
async def lifespan(_: FastAPI):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, run_migrations)
    yield
