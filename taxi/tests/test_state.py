import httpx
import pytest
import respx
from unittest.mock import AsyncMock, patch
from urllib.parse import urljoin

from app.config import settings
from app.schemas.trip import TripPostRequest
from app.state import TaxiState


@pytest.mark.asyncio
async def test_state_randomize_state_available():
    taxi_state = TaxiState()

    with patch.object(
        taxi_state, "_delayed_mark_available", new_callable=AsyncMock
    ) as mock_delayed:
        taxi_state.randomize_state(seed=42)

        mock_delayed.assert_not_called()

    assert taxi_state.available is True
    assert taxi_state.x == 82
    assert taxi_state.y == 15


@pytest.mark.asyncio
async def test_state_randomize_state_unavailable():
    taxi_state = TaxiState()

    with patch.object(
        taxi_state, "_delayed_mark_available", new_callable=AsyncMock
    ) as mock_delayed:
        taxi_state.randomize_state(seed=111)

        mock_delayed.assert_called_once_with(9.855220838931789)

    assert taxi_state.available is False
    assert taxi_state.x == 28
    assert taxi_state.y == 41


@pytest.mark.asyncio
@respx.mock
async def test_state_handle_trip():
    taxi_state = TaxiState()
    taxi_state.taxi_id = "test-taxi-id-1"
    taxi_state.x = 50
    taxi_state.y = 50
    taxi_state._speed_lower_boundary = 0
    taxi_state._speed_upper_boundary = 0

    trip_request = TripPostRequest(
        x_start=60,
        y_start=40,
        x_stop=30,
        y_stop=90,
    )
    DISPATCH_URL = str(settings.dispatch_url)

    route_picked = respx.post(urljoin(DISPATCH_URL, "/event/picked")).mock(
        httpx.Response(status_code=204)
    )
    route_dropped = respx.post(urljoin(DISPATCH_URL, "/event/dropped")).mock(
        httpx.Response(status_code=204)
    )

    await taxi_state.handle_trip(trip_request)

    assert route_picked.call_count == 1
    request: httpx.Request = route_picked.calls[0].request
    assert request.content == b'{"taxi_id":"test-taxi-id-1"}'

    assert route_dropped.call_count == 1
    request: httpx.Request = route_dropped.calls[0].request
    assert request.content == b'{"taxi_id":"test-taxi-id-1"}'

    assert taxi_state.is_available is True
