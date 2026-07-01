from src.info import APIAdapter


def test_api_adapter():
    api = APIAdapter()
    assert api.aeroplanes is None or len(api.aeroplanes) == 0


def test_api_adapter_url():
    api = APIAdapter()
    assert "openstreetmap" in api.openstreetmap_url
    assert "opensky-network" in api.opensky_url
