import logging
from typing import AsyncGenerator

from alembic import command as alembic_command
from alembic.config import Config
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=settings.postgres_user,
    password=settings.postgres_password,
    host=settings.postgres_host,
    port=5432,
    database=settings.postgres_db,
)


engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


def run_migrations() -> None:
    logger.info("Running Alembic migrations...")
    alembic_cfg = Config("alembic.ini")
    alembic_command.upgrade(alembic_cfg, "head")
    logger.info("Migrations completed.")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
