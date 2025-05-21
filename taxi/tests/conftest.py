import httpx
import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.main import app
from app.state import TaxiState, get_taxi_state


@pytest.fixture
def busy_taxi_state():
    state = TaxiState()
    state.mark_busy()
    return state


@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client_with_busy_taxi(busy_taxi_state):
    app.dependency_overrides[get_taxi_state] = lambda: busy_taxi_state
    async with AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
