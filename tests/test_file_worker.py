import json
import os

from src.airplane import Airplane
from src.file_worker import JSONPlane


def test_json_plane():
    data = JSONPlane("test_plane.json")
    assert "data" in data.filename
    assert "test_plane.json" in data.filename


def test_json_plane_add_airplane():
    test_file = "temp_add_test.json"
    full_path = os.path.join("data", test_file)
    storage = JSONPlane(test_file)
    plane = Airplane("France", "AFR777", 900, 10000)
    storage.add_airplane(plane)
    with open(full_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1
    assert data[0]["name"] == "AFR777"
    assert data[0]["country"] == "France"
    os.remove(full_path)
