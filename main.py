from src.info import APIAdapter


def main():
    api = APIAdapter()
    print("=== Мониторинг воздушного пространства ===")
    print("\nПроверка подключения к API Nominatim и OpenSky...")
    if not api.connect():
        print("Ошибка: Нет связи с серверами. Проверьте интернет-соединение.")
        return

    country = input("\nВведите название страны на английском (например, Canada, France, Germany): ").strip()

    if not country:
        print("Название страны не может быть пустым.")
        return

    print(f"\nВыполняется поиск самолетов для страны: {country}...")
    api.get_aeroplanes(country)

    if api.aeroplanes and "states" in api.aeroplanes and api.aeroplanes["states"]:
        flights = api.aeroplanes["states"]
        print(f"\n[УСПЕХ] В воздушном пространстве страны {country} сейчас находится самолетов: {len(flights)}")
        print("-" * 70)
        print(f"{'Позывной/Рейс':<15} | {'Страна борта':<20} | {'Высота (м)':<12} | {'На земле':<8}")
        print("-" * 70)

        for flight in flights[:10]:
            callsign = flight[1].strip() if flight[1] else "UNKNOWN"
            origin_country = flight[2] if flight[2] else "UNKNOWN"
            altitude = flight[7] if flight[7] is not None else "N/A"
            on_ground = "Да" if flight[8] else "Нет"

            print(f"{callsign:<15} | {origin_country:<20} | {altitude:<12} | {on_ground:<8}")

        if len(flights) > 10:
            print(f"... и еще {len(flights) - 10} самолетов.")
    else:
        print(f"\n[ИНФО] В выбранном регионе ({country}) сейчас нет активных самолетов или страна не найдена.")


if __name__ == "__main__":
    main()