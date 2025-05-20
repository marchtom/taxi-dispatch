from copy import deepcopy

import pytest

from app.models import TaxiModel, TripModel

from .test_data import taxi, trip


@pytest.mark.asyncio
async def test_event_picked(client, db_session):
    taxi_id = "id-1"
    taxi_dict = deepcopy(taxi.taxi_1)
    taxi_dict["id"] = taxi_id
    taxi_entity = TaxiModel.create(**taxi_dict)
    db_session.add(taxi_entity)

    trip_dict = deepcopy(trip.trip_1)
    trip_dict["taxi_id"] = taxi_id
    trip_entity = TripModel.create(**trip_dict)
    db_session.add(trip_entity)

    resp = await client.post(
        "/event/picked",
        json={"taxi_id": taxi_id},
    )
    assert resp.status_code == 200
    assert resp.json() == {"message": "ok"}

    resp_trip = await client.get(f"/trip/{trip_entity.id}")
    assert resp_trip.status_code == 200
    assert resp_trip.json()["pickup_time"] is not None


@pytest.mark.asyncio
async def test_event_dropped(client, db_session):
    taxi_dict = deepcopy(taxi.taxi_1)
    taxi_dict["available"] = False
    taxi_entity = TaxiModel.create(**taxi_dict)
    db_session.add(taxi_entity)

    trip_dict = deepcopy(trip.trip_1)
    trip_dict["taxi_id"] = taxi_entity.id
    trip_entity = TripModel.create(**trip_dict)
    db_session.add(trip_entity)

    await db_session.flush()

    resp = await client.post(
        "/event/dropped",
        json={"taxi_id": taxi_entity.id},
    )
    assert resp.status_code == 200
    assert resp.json() == {"message": "ok"}

    # check taxi status, should be available with new x, y
    resp_taxi = await client.get(f"/taxi/{taxi_entity.id}")
    assert resp_taxi.status_code == 200
    assert resp_taxi.json() == {
        "available": True,
        "callback_url": "http://callback-1.url",
        "id": "test-taxi-id-1",
        "x": trip_dict["x_stop"],
        "y": trip_dict["y_stop"],
    }

    # trip should be finalized
    resp_trip = await client.get(f"/trip/{trip_entity.id}")
    assert resp_trip.json()["end_time"] is not None
