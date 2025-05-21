import pytest


@pytest.mark.asyncio
async def test_taxi_root(client):
    resp = await client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"Taxi": "OK"}


@pytest.mark.asyncio
async def test_taxi_is_busy_error(client_with_busy_taxi):
    resp = await client_with_busy_taxi.post(
        "/trip",
        json={
            "x_start": 10,
            "y_start": 20,
            "x_stop": 5,
            "y_stop": 99,
        },
    )
    assert resp.status_code == 503
    assert resp.json() == {"detail": "Taxi is busy, try again later."}
