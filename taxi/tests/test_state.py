import pytest
from unittest.mock import AsyncMock, patch

from app.state import TaxiState


@pytest.mark.asyncio
async def test_state_randomize_state_available():
    taxi_state = TaxiState()

    with patch.object(
        taxi_state, '_delayed_mark_available', new_callable=AsyncMock
    ) as mock_delayed:
        taxi_state.randomize_state(seed=42)

        mock_delayed.assert_not_called()

    assert taxi_state.available is True
    assert taxi_state.x == 82
    assert taxi_state.y == 15


@pytest.mark.asyncio
async def test_state_randomize_state_available():
    taxi_state = TaxiState()

    with patch.object(
        taxi_state, '_delayed_mark_available', new_callable=AsyncMock
    ) as mock_delayed:
        taxi_state.randomize_state(seed=111)

        mock_delayed.assert_called_once_with(9.855220838931789)

    assert taxi_state.available is False
    assert taxi_state.x == 28
    assert taxi_state.y == 41
