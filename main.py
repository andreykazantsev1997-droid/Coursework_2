from src.info import APIAdapter
from src.file_worker import JSONPlane

def print_menu():
    print("\n" + "="*40)
    print("УПРАВЛЕНИЕ ВОЗДУШНЫМ ПРОСТРАНСТВОМ")
    print("="*40)
    print("1. Загрузить данные по стране (OpenSky API)")
    print("2. Показать ТОП самолетов по ВЫСОТЕ полета")
    print("3. Фильтр: Найти самолеты по стране регистрации")
    print("4. Сохранить все текущие самолеты в JSON-файл")
    print("0. Выход из программы")
    print("="*40)

def main():
    api = APIAdapter()
    storage = JSONPlane()
    print("=== Мониторинг воздушного пространства ===")
    print("\nПроверка подключения к API Nominatim и OpenSky...")
    if not api.connect():
        return

    while True:
        print_menu()
        choice = input("Выберите пункт: ").strip()
        if choice == "1":
            country = input("\nВведите название страны на английском (например, Canada, France, Germany): ").strip()
            api.get_aeroplanes(country)

        elif choice == "2":
            if not api.aeroplanes:
                print("\nСначала загрузите данные (Пункт 1). Список пуст.")
                continue

            try:
                n = int(input(f"\nВведите количество самолетов N (доступно всего {len(api.aeroplanes)}): "))
                if n <= 0:
                    print("Число должно быть больше нуля.")
                    continue
                sorted_by_altitude = sorted(api.aeroplanes, reverse=True)
                top_n = sorted_by_altitude[:n]
                print(f"\n=== ТОП {len(top_n)} САМОЛЕТОВ ПО ХАРАКТЕРИСТИКАМ ===")
                for p in top_n:
                    print(f"Рейс: {p._name:<10} | Высота: {p._altitude_fly:<8.2f} | Скорость: {p._speed_fly:<8.2f} м/с | Борт: {p._country}")

            except ValueError:
                print("Ошибка! Нужно ввести целое число.")

        elif choice == "3":
            if not api.aeroplanes:
                print("\nСначала загрузите данные (Пункт 1). Список пуст.")
                continue
            reg_country = input("\nВведите страну регистрации борта (например, 'United States', 'Germany'): ").strip()
            filtered_planes = [p for p in api.aeroplanes if reg_country.lower() in p._country.lower()]
            if filtered_planes:
                print(f"\n=== Найдено самолетов страны {reg_country}: {len(filtered_planes)} ===")
                for p in filtered_planes:
                    print(f"Рейс: {p._name:<10} | Борт: {p._country:<20} | Высота: {p._altitude_fly:<8.2f} м")
            else:
                print(f"\nСамолеты с регистрацией в '{reg_country}' не найдены в текущем списке")

        elif choice == "4":
            if not api.aeroplanes:
                print("\nНет данных для сохранения. Сначала выполните поиск (Пункт 1)")
                continue

            for p in api.aeroplanes:
                storage.add_airplane(p)
            print(f"\nВсе самолеты ({len(api.aeroplanes)} шт.) записаны в JSON")

        elif choice == "0":
            print("\nПрограмма завершена")
            break
        else:
            print("\nНеверный пункт меню")

if __name__ == "__main__":
    main()