from src.info import APIAdapter


def test_api_adapter():
    api = APIAdapter()
    assert api.aeroplanes is None or len(api.aeroplanes) == 0


def test_api_adapter_url():
    api = APIAdapter()
    assert "openstreetmap" in api.openstreetmap_url
    assert "opensky-network" in api.opensky_url


def test_api_adapter_connect_error_branch():
    api = APIAdapter()
    api.openstreetmap_url = "https://broken-url-that-does-not-exist-12345.org"
    result = api.connect()
    assert result is False


def test_get_aeroplanes_empty_country(capsys):
    api = APIAdapter()
    api.get_aeroplanes("   ")
    assert api.aeroplanes == []
    captured = capsys.readouterr()
    assert "Ошибка: запрос не может быть пустым." in captured.out


def test_get_aeroplanes_nominatim_json_error(mocker, capsys):
    api = APIAdapter()
    mock_resp = mocker.Mock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.side_effect = ValueError("Incomplete JSON")
    mocker.patch("requests.get", return_value=mock_resp)
    api.get_aeroplanes("France")
    assert api.aeroplanes == []
    captured = capsys.readouterr()
    assert "Ошибка при запросе к Nominatim" in captured.out
