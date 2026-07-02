from abc import ABC, abstractmethod

import requests

from src.airplane import Airplane


class GetInfo(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_aeroplanes(self, country):
        pass


class APIAdapter(GetInfo):
    def __init__(self):
        self.openstreetmap_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all?"
        self.aeroplanes = None

    def connect(self):
        headers = {
            "User-Agent": "test-app/1.0",
        }
        try:
            geo_res = requests.get(
                self.openstreetmap_url,
                params={"q": "London", "format": "json", "limit": 1},
                headers=headers,
                timeout=5,
            )
            sky_res = requests.get(
                self.opensky_url,
                params={"lamin": 0, "lamax": 1, "lomin": 0, "lomax": 1},
                timeout=5,
            )
            if geo_res.status_code == 200 and sky_res.status_code == 200:
                print("Успешное подключение к API")
                return True
            print(
                f"Один из сервисов вернул ошибку. Nominatim: {geo_res.status_code}, OpenSky: {sky_res.status_code}"
            )
            return False
        except requests.RequestException as e:
            print(f"Ошибка при подключении к API: {e}")
            return False

    def get_aeroplanes(self, country):
        if not country or not country.strip():
            print("Ошибка: запрос не может быть пустым.")
            self.aeroplanes = []
            return

        headers_nominatim = {
            "User-Agent": "test-app/1.0",
        }
        params_nominatim = {
            "country": country,
            "format": "json",
            "limit": 1,
        }
        try:
            response = requests.get(
                url=self.openstreetmap_url,
                params=params_nominatim,
                headers=headers_nominatim,
            )
            data = response.json()

        except (requests.RequestException, ValueError) as e:
            print(f"Ошибка при запросе к Nominatim: {e}")
            self.aeroplanes = []
            return

        geo_coordinates = data[0].get("boundingbox")
        if not geo_coordinates or len(geo_coordinates) < 4:
            print("Некорректные данные boundingbox от Nominatim")
            self.aeroplanes = []
            return

        try:
            params = {
                "lamin": float(geo_coordinates[0]),
                "lamax": float(geo_coordinates[1]),
                "lomin": float(geo_coordinates[2]),
                "lomax": float(geo_coordinates[3]),
            }
        except (ValueError, TypeError) as e:
            print(f"Ошибка конвертации координат boundingbox: {e}")
            self.aeroplanes = []
            return

        try:
            response = requests.get(self.opensky_url, params=params, timeout=5)
            response.raise_for_status()
            res_data = response.json()

        except (requests.RequestException, ValueError) as e:
            print(f"Ошибка при запросе к OpenSky: {e}")
            self.aeroplanes = []
            return

        if not res_data or not isinstance(res_data, dict):
            print("Получен пустой или некорректный ответ от OpenSky")
            self.aeroplanes = []
            return

        states = res_data.get("states")
        self.aeroplanes = []

        if states:
            for state in states:
                if not isinstance(state, list) or len(state) < 8:
                    continue

                try:
                    plane = Airplane(
                        country=state[2],
                        name=state[1],
                        speed_fly=state[9],
                        altitude_fly=state[7],
                    )
                    self.aeroplanes.append(plane)
                except Exception as e:
                    print(f"Ошибка создания объекта для {state[1]}: {e}")
                    continue

            print(f"Данные успешно преобразованы. Найдено: {len(self.aeroplanes)}")
        else:
            print(
                "В указанном регионе в данный момент нет самолетов (список states пуст)."
            )
