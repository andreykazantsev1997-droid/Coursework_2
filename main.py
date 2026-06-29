from src.info import APIAdapter


def main():
    api = APIAdapter()
    print("=== Мониторинг воздушного пространства ===")
    print("\nПроверка подключения к API Nominatim и OpenSky...")
    if not api.connect():
        return

    country = input("\nВведите название страны на английском (например, Canada, France, Germany): ").strip()
    if not country:
        return

    print(f"\nВыполняется поиск самолетов для страны: {country}...")
    api.get_aeroplanes(country)

    if api.aeroplanes:
        print(f"\n[УСПЕХ] В воздушном пространстве страны {country} сейчас находится самолетов: {len(api.aeroplanes)}")
        sorted_planes = sorted(api.aeroplanes, reverse=True)
        print("-" * 80)
        print(f"{'Позывной/Рейс':<15} | {'Страна борта':<20} | {'Скорость (м/с)':<15} | {'Высота (м)':<12}")
        print("-" * 80)

        for plane in sorted_planes:
            print(
                f"{plane._name:<15} | {plane._country:<20} | {plane._speed_fly:<15.2f} | {plane._altitude_fly:<12.2f}")

            # Демонстрация сравнения двух объектов (требование ТЗ)
        if len(sorted_planes) >= 2:
            print("\n=== Демонстрация работы методов сравнения ===")
            p1 = sorted_planes[0]
            p2 = sorted_planes[1]
            print(f"Самый быстрый самолет: {p1._name} со скоростью {p1._speed_fly} м/с")
            print(f"Второй по скорости: {p2._name} со скоростью {p2._speed_fly} м/с")
            print(f"Результат проверки (Первый быстрее Второго?): {p1 > p2}")
    else:
        print(f"\n[ИНФО] В выбранном регионе ({country}) сейчас нет активных самолетов или страна не найдена.")

if __name__ == "__main__":
    main()