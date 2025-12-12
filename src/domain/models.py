from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class WeatherPeriod:
    title: str
    temperature: int
    pressure_mm: int
    humidity_percent: int
    condition: str


@dataclass
class WeatherDay:
    date: str
    magnetic_field: int  # 1-5 (шкала Яндекса)
    periods: List[WeatherPeriod]

    @property
    def daytime_periods(self) -> List[WeatherPeriod]:
        return [p for p in self.periods if p.title in ("утро", "день", "вечер")]

    @property
    def avg_day_temp(self) -> float:
        temps = [p.temperature for p in self.daytime_periods]
        return round(sum(temps) / len(temps), 1) if temps else 0.0

    @property
    def pressure_change_alert(self) -> str:
        pressures = [p.pressure_mm for p in self.periods]
        if len(pressures) < 2:
            return ""
        min_p, max_p = min(pressures), max(pressures)
        diff = max_p - min_p
        if diff >= 5:
            return "ожидается резкое увеличение атмосферного давления"
        elif diff <= -5:
            return "ожидается резкое падение атмосферного давления"
        return ""


@dataclass
class WeatherReport:
    city: str
    days: List[WeatherDay]