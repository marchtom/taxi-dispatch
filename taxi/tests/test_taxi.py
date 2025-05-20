import pytest


@pytest.mark.asyncio
async def test_dispatch_root(client):
    resp = await client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"Taxi": "OK"}



