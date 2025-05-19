from datetime import datetime

import pytest

from app.models import TripModel


@pytest.mark.asyncio
async def test_trip_get_single(
        db_session,
        client,
    ):
    datetime_str = "2025-05-20T00:00:00+02:00"
    expected_item = {
        "id": "1",
        "start_time": datetime.fromisoformat(datetime_str),
        "x_start": 1,
        "y_start": 2,
        "x_stop": 3,
        "y_stop": 4,
    }
    entity = TripModel.create(**expected_item)
    expected_item["start_time"] = datetime_str
    expected_item["end_time"] = None
    db_session.add(entity)
    await db_session.flush()

    resp = await client.get(f"/trip/{entity.id}")
    assert resp.status_code == 200
    assert resp.json() == expected_item


@pytest.mark.asyncio
async def test_trip_get_missing(client):
    resp = await client.get("/trip/missing-id")
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'Trip.ID: `missing-id` not found.'}


@pytest.mark.asyncio
async def test_trip_create(client):
    payload = {
        "id": "trip-id-1",
        "start_time": "2025-05-20T00:00:00+02:00",
        "x_start": 10,
        "y_start": 20,
        "x_stop": 5,
        "y_stop": 99,
    }
    resp = await client.post(
        "/trip",
        json=payload,
    )
    assert resp.status_code == 200
    assert resp.json() == {"id": "trip-id-1"}

    resp_get = await client.get(f"/trip/{payload['id']}")
    assert resp_get.status_code == 200
    assert resp_get.json() == {
        "id": "trip-id-1",
        "start_time": "2025-05-19T22:00:00Z",
        "end_time": None,
        "x_start": 10,
        "y_start": 20,
        "x_stop": 5,
        "y_stop": 99,
    }


@pytest.mark.asyncio
async def test_trip_update(
        db_session,
        client,
    ):
    datetime_str = "2025-05-20T00:00:00+02:00"
    end_time = "2025-05-20T00:12:30Z"
    expected_item = {
        "id": "1",
        "start_time": datetime.fromisoformat(datetime_str),
        "x_start": 1,
        "y_start": 2,
        "x_stop": 3,
        "y_stop": 4,
    }
    entity = TripModel.create(**expected_item)
    expected_item["start_time"] = datetime_str
    expected_item["end_time"] = end_time
    db_session.add(entity)
    await db_session.flush()

    resp = await client.patch(
        f"/trip/{entity.id}",
        json={"end_time": end_time},
    )
    assert resp.status_code == 200
    assert resp.json() == {"id": "1"}

    resp_get = await client.get(f"/trip/{entity.id}")
    assert resp_get.status_code == 200
    assert resp_get.json() == expected_item
