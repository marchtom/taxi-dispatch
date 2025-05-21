from copy import deepcopy

import pytest

from app.models import TaxiModel

from .test_data import taxi


@pytest.mark.asyncio
async def test_taxi_get_list_none(client):
    resp = await client.get("/taxi")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_taxi_get_single(
    db_session,
    client,
):
    expected_item = deepcopy(taxi.taxi_1)
    entity = TaxiModel.create(**expected_item)
    db_session.add(entity)
    await db_session.flush()

    resp = await client.get(f"/taxi/{entity.id}")
    assert resp.status_code == 200
    assert resp.json() == expected_item


@pytest.mark.asyncio
async def test_taxi_get_missing(client):
    resp = await client.get("/taxi/missing-id")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Taxi.ID: `missing-id` not found."}


@pytest.mark.asyncio
async def test_taxi_create(client):
    payload = {
        "id": "id-1",
        "callback_url": "http://callback.url",
        "available": True,
        "x": 20,
        "y": 42,
    }
    resp = await client.post(
        "/taxi",
        json=payload,
    )
    assert resp.status_code == 200
    assert resp.json() == {"id": "id-1"}

    resp_get = await client.get(f"/taxi/{payload['id']}")
    assert resp_get.status_code == 200
    assert resp_get.json() == payload


@pytest.mark.asyncio
async def test_taxi_patch(
    db_session,
    client,
):
    expected_item = deepcopy(taxi.taxi_1)
    expected_item["available"] = False
    entity = TaxiModel.create(**expected_item)
    db_session.add(entity)
    await db_session.flush()

    resp = await client.patch(f"/taxi/{entity.id}", json={"available": True})
    assert resp.status_code == 200

    resp_get = await client.get(f"/taxi/{entity.id}")
    assert resp_get.status_code == 200
    assert resp_get.json()["available"] is True
