import json
import os
from src.airplane import Airplane
from src.file_worker import JSONPlane


def test_json_plane():
    data = JSONPlane("test_plane.json")
    assert "data" in data.filename
    assert "test_plane.json" in data.filename
    if os.path.exists(data.filename):
        os.remove(data.filename)


def test_json_plane_add_airplane():
    test_file = "temp_add_test.json"
    full_path = os.path.join("data", test_file)
    if os.path.exists(full_path):
        os.remove(full_path)
    storage = JSONPlane(test_file)
    plane = Airplane("France", "AFR777", 900, 10000)
    assert storage.add_airplane(plane) is True
    with open(full_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1
    assert data[0]["name"] == "AFR777"
    assert data[0]["country"] == "France"
    if os.path.exists(full_path):
        os.remove(full_path)


def test_json_plane_duplicate_prevent():
    test_file = "temp_duplicate_test.json"
    full_path = os.path.join("data", test_file)
    if os.path.exists(full_path):
        os.remove(full_path)
    storage = JSONPlane(test_file)
    plane = Airplane(country="France", name="AFR777", speed_fly=900, altitude_fly=10000)
    res1 = storage.add_airplane(plane)
    res2 = storage.add_airplane(plane)
    assert res1 is True
    assert res2 is False
    with open(full_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 1
    if os.path.exists(full_path):
        os.remove(full_path)


def test_file_worker_get_stub():
    storage = JSONPlane("test_coverage.json")
    result = storage.get_airplane({"country": "Any"})
    assert result == []
    if os.path.exists(storage.filename):
        os.remove(storage.filename)


def test_file_worker_delete_stub():
    storage = JSONPlane("test_coverage.json")
    result = storage.delete_airplane({"country": "Any"})
    assert result is False
    if os.path.exists(storage.filename):
        os.remove(storage.filename)
