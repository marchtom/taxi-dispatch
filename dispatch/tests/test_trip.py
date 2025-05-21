from copy import deepcopy

import httpx
import pytest
import respx

from app.models import TaxiModel, TripModel

from .test_data import taxi, trip


@pytest.mark.asyncio
async def test_trip_get_single(
    db_session,
    client,
):
    # FIXME: need ModelFactory, seed creation is too messy
    datetime_str = deepcopy(trip.datetime_str)
    expected_item = deepcopy(trip.trip_1)
    entity = TripModel.create(**expected_item)
    expected_item["start_time"] = datetime_str
    expected_item["pickup_time"] = None
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
    assert resp.json() == {"detail": "Trip.ID: `missing-id` not found."}


@pytest.mark.asyncio
@respx.mock
async def test_trip_create(
    client,
    db_session,
):
    # create at least one available taxi
    taxi_entity = TaxiModel.create(**deepcopy(taxi.taxi_1))
    db_session.add(taxi_entity)
    await db_session.flush()

    # configure respx capture for taxi's callback_url
    route = respx.post(taxi.taxi_1["callback_url"]).mock(httpx.Response(status_code=204))

    payload_trip = {
        "id": "trip-id-1",
        "start_time": "2025-05-19T22:00:00Z",
        "x_start": 10,
        "y_start": 20,
        "x_stop": 5,
        "y_stop": 99,
    }
    resp = await client.post(
        "/trip",
        json=payload_trip,
    )
    assert resp.status_code == 200
    assert resp.json() == {"id": "trip-id-1"}

    resp_get = await client.get(f"/trip/{payload_trip['id']}")
    assert resp_get.status_code == 200
    payload_trip["pickup_time"] = None
    payload_trip["end_time"] = None
    assert resp_get.json() == payload_trip

    # check calls made by TaxiService.order_trip()
    assert route.call_count == 1
    request: httpx.Request = route.calls[0].request
    assert request.content == b'{"x_start":10,"y_start":20,"x_stop":5,"y_stop":99}'


@pytest.mark.asyncio
@respx.mock
async def test_trip_create_no_available_taxi(
    client,
    db_session,
    mock_taxi_service,
):
    # the only existing taxi is busy
    taxi_dict = deepcopy(taxi.taxi_1)
    taxi_dict["available"] = False
    taxi_entity = TaxiModel.create(**taxi_dict)
    db_session.add(taxi_entity)
    await db_session.flush()

    payload_trip = {
        "id": "trip-id-1",
        "start_time": "2025-05-19T22:00:00Z",
        "x_start": 10,
        "y_start": 20,
        "x_stop": 5,
        "y_stop": 99,
    }
    resp = await client.post(
        "/trip",
        json=payload_trip,
    )
    assert resp.status_code == 503
    assert resp.json() == {"detail": "We are sorry, all the taxies are busy at the moment."}

    mock_taxi_service.assert_not_awaited()


@pytest.mark.asyncio
async def test_trip_update(
    db_session,
    client,
):
    expected_item = deepcopy(trip.trip_1)
    entity = TripModel.create(**expected_item)
    db_session.add(entity)
    await db_session.flush()

    datetime_str = deepcopy(trip.datetime_str)
    expected_item["start_time"] = datetime_str
    end_time = "2025-05-20T00:12:30Z"
    expected_item["pickup_time"] = None
    expected_item["end_time"] = end_time

    resp = await client.patch(
        f"/trip/{entity.id}",
        json={"end_time": end_time},
    )
    assert resp.status_code == 200
    assert resp.json() == {"id": "1"}

    resp_get = await client.get(f"/trip/{entity.id}")
    assert resp_get.status_code == 200
    assert resp_get.json() == expected_item
