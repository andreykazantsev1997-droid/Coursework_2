from src.airplane import Airplane


def test_airplane_creation():
    plane = Airplane(" France ", "AFR123", "850", "10000")
    assert plane._country == "France"
    assert plane._name == "AFR123"
    assert plane._speed_fly == 850.0


def test_airplane_comparison():
    slow_plane = Airplane("Germany", "DLH1", 700, 10000)
    fast_plane = Airplane("Germany", "DLH2", 900, 10000)
    assert slow_plane < fast_plane


def test_airplane_equality():
    first_plane = Airplane("Germany", "DLH1", 900, 10000)
    second_plane = Airplane("Germany", "DLH2", 900, 10000)
    assert first_plane == second_plane


def test_airplane_invalid_data_validation():
    bad_plane = Airplane(123, "   ", "not_a_number", None)
    assert bad_plane._country == "UNKNOWN"
    assert bad_plane._name == "UNKNOWN"
    assert bad_plane._speed_fly == 0.0
    assert bad_plane._altitude_fly == 0.0


def test_airplane_comparison_with_wrong_type():
    plane = Airplane("France", "AFR101", 800, 11000)
    wrong_object = "Строка"
    assert (plane == wrong_object) is False
    try:
        _ = plane < wrong_object
    except TypeError:
        pass
