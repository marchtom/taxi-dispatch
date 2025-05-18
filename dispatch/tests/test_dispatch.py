import pytest


def test_dispatch_root(application):
    resp = application.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"Dispatch": "OK"}


# @pytest.mark.usefixtures("db_session")
# def test_dispatch_taxi_get(application):
#     resp = application.get("/taxi")
#     assert resp.status_code == 200
#     assert resp.json() == {"Dispatch": "OK"}


@pytest.mark.usefixtures("db_session")
def test_dispatch_taxi_create(application):
    payload = {
        "id": "id-1",
        "callback_url": "http://callback.url",
        "active": True,
        "x": 20,
        "y": 42,
    }
    resp = application.post(
        "/taxi",
        json=payload,
    )
    assert resp.status_code == 200
    assert resp.json() == {"Dispatch": "OK"}
