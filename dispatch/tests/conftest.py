import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.main import app
from app.db import Base, get_db
from alembic.config import Config
from alembic import command


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://dispatch:dispatch@localhost:5432/dispatch_test")


@pytest.fixture(scope="session")
async def migrated_postgres():
    alembic_cfg = Config("dispatch/alembic.ini")
    command.upgrade(alembic_cfg, "head")
    yield


@pytest.fixture(scope="function")
async def db_session(migrated_postgres):
    engine = create_async_engine(DATABASE_URL, future=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        yield session

        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE;')

        await session.commit()


@pytest.fixture
def application(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as c:
        yield c
