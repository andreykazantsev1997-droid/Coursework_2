from abc import ABC, abstractmethod
import json
import os
from src.airplane import Airplane

class PlaneStorage(ABC):
    @abstractmethod
    def add_airplane(self, plane):
        pass

    @abstractmethod
    def get_airplane(self, criteria):
        pass

    @abstractmethod
    def delete_airplane(self, criteria):
        pass

class JSONPlane(PlaneStorage):
    def __init__(self, filename="airplane.json"):
        folder_name = "data"
        self.filename = os.path.join(folder_name, filename)
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([], f)

    def add_airplane(self, plane):
        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        plane_dict = {
            "country": plane._country,
            "name": plane._name,
            "speed_fly": plane._speed_fly,
            "altitude_fly": plane._altitude_fly
        }
        data.append(plane_dict)

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Самолет {plane._name} успешно сохранен в файл.")

    def get_airplane(self, criteria):
        print("Метод поиска по критериям пока не используется")
        return []

    def delete_airplane(self, criteria):
        print("Метод удаления пока не используется")
        return False
