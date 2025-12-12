from src.domain.models import WeatherReport, WeatherDay, WeatherPeriod

class YandexResponseMapper:
    def to_weather_report(self, raw_data: dict, city: str) -> WeatherReport:
        # Для демо — mock
        days = []
        for i in range(7):
            periods = [
                WeatherPeriod("ночь", -2, 750, 80, "ясно"),
                WeatherPeriod("утро", 0, 752, 75, "облачно"),
                WeatherPeriod("день", 3, 755, 70, "снег"),
                WeatherPeriod("вечер", 1, 753, 78, "пасмурно"),
            ]
            day = WeatherDay(
                date=f"2025-12-{7+i:02d}",
                magnetic_field=2,
                periods=periods
            )
            days.append(day)
        return WeatherReport(city=city, days=days)