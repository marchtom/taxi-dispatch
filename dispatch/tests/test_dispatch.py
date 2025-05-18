def test_dispatch_root(application):
    resp = application.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"Dispatch": "OK"}
