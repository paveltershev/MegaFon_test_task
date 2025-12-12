import sys
import os
from datetime import datetime
from openpyxl import Workbook

def parse_weather_from_file(filepath: str):
    with open(filepath, encoding="utf-8") as f:
        lines = [line.rstrip("\n\r") for line in f]


    period_lines = []
    for i, line in enumerate(lines):
        if line.startswith("- Утром") or line.startswith("- Днём") or line.startswith("- Вечером") or line.startswith("- Ночью"):
            period_lines.append(i)

    data = []
    for idx in period_lines:
        try:
            period = lines[idx][2:].strip()  # "- Утром" → "Утром"
            temp = lines[idx + 1][2:].strip() if lines[idx + 1].startswith("- ") else None
            condition = lines[idx + 2][2:].strip() if lines[idx + 2].startswith("- ") else None
            feels = lines[idx + 3][2:].strip() if lines[idx + 3].startswith("- ") else None
            wind_num = lines[idx + 4][2:].strip() if lines[idx + 4].startswith("- ") else None
            wind_str = lines[idx + 5][2:].strip() if lines[idx + 5].startswith("- ") else None
            humidity = lines[idx + 6][2:].strip() if lines[idx + 6].startswith("- ") else None
            pressure = lines[idx + 7][2:].strip() if lines[idx + 7].startswith("- ") else None

            if temp and feels and "°" in temp and "°" in feels:
                data.append({
                    "period": period,
                    "temperature": temp,
                    "feels_like": feels,
                    "condition": condition,
                    "wind": wind_str,
                    "humidity": humidity,
                    "pressure_mmHg": pressure
                })
        except IndexError:
            continue
    return data

def export_to_excel(data, filename):
    wb = Workbook()
    ws = wb.active
    ws.title = "Прогноз погоды"
    headers = ["Период", "Температура", "Ощущается как", "Погода", "Ветер", "Влажность", "Давление (мм рт.ст.)"]
    ws.append(headers)
    for row in data:
        ws.append([
            row["period"],
            row["temperature"],
            row["feels_like"],
            row["condition"],
            row["wind"],
            row["humidity"],
            row["pressure_mmHg"]
        ])
    wb.save(filename)

def log_request(city, success, error=None):
    import sqlite3
    conn = sqlite3.connect("weather_requests.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS weather_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            success BOOLEAN NOT NULL,
            error TEXT,
            timestamp TEXT NOT NULL
        )
    """)
    cur.execute(
        "INSERT INTO weather_requests (city, success, error, timestamp) VALUES (?, ?, ?, ?)",
        (city, success, error, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def main():
    if len(sys.argv) < 2:
        print("Использование: python main.py \"Город\"")
        return

    city = sys.argv[1].strip()
    print(f"Обработка запроса для города: {city}")

    try:
        sample_path = os.path.join(os.path.dirname(__file__), "..", "samples", "yandex_moscow.html")
        weather_data = parse_weather_from_file(sample_path)
        print(f"Найдено {len(weather_data)} записей о погоде")

        if not weather_data:
            raise ValueError("Не удалось извлечь данные")

        filename = f"weather_report_{city}.xlsx"
        export_to_excel(weather_data, filename)
        log_request(city, success=True)
        print(f"Успешно! Данные сохранены в {filename}")
    except Exception as e:
        log_request(city, success=False, error=str(e))
        print(f" Ошибка: {e}")

if __name__ == "__main__":
    main()