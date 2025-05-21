import pathlib
from unittest.mock import AsyncMock

import httpx
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config
from app.db import DATABASE_URL, Base, get_db
from app.dependencies import get_taxi_service
from app.main import app
from app.services import TaxiService


@pytest.fixture(scope="session")
def apply_migrations():
    base_dir = pathlib.Path(__file__).resolve().parent.parent
    path_to_cfg = str(base_dir / "alembic.ini")
    alembic_cfg = Config(path_to_cfg)

    alembic_upgrade(alembic_cfg, "head")


@pytest.fixture
async def db_session(apply_migrations):
    engine = create_async_engine(DATABASE_URL, future=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        yield session

        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE;'))

        await session.commit()


@pytest.fixture
def mock_taxi_service(monkeypatch):
    mock = AsyncMock(spec=TaxiService)
    monkeypatch.setattr("app.dependencies.get_taxi_service", lambda: mock)
    app.dependency_overrides[get_taxi_service] = lambda: mock
    return mock


@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    async with AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
