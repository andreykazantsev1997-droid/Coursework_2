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
        headers_nominatim = {
            "User-Agent": "test-app/1.0",
        }
        params_nominatim = {
            "country": country,
            "format": "json",
            "limit": 1,
        }
        response = requests.get(
            url=self.openstreetmap_url,
            params=params_nominatim,
            headers=headers_nominatim,
        )
        data = response.json()
        if not data:
            print(f"Страна {country} не найдена")
            self.aeroplanes = []
            return
        geo_coordinates = data[0].get("boundingbox")
        params = {
            "lamin": float(geo_coordinates[0]),
            "lamax": float(geo_coordinates[1]),
            "lomin": float(geo_coordinates[2]),
            "lomax": float(geo_coordinates[3]),
        }
        response = requests.get(url=self.opensky_url, params=params)

        if response.status_code == 200:
            res_data = response.json()
            states = res_data.get("states")
            self.aeroplanes = []
            if states:
                for state in states:
                    plane = Airplane(
                        country=state[2],
                        name=state[1],
                        speed_fly=state[9],
                        altitude_fly=state[7],
                    )
                    self.aeroplanes.append(plane)
            print(
                f"Данные успешно преобразованы в объекты Airplane. Найдено: {len(self.aeroplanes)}"
            )
        else:
            print(
                f"Не удалось получить данные от OpenSky. Код ответа: {response.status_code}"
            )
            self.aeroplanes = []
