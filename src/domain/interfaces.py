from abc import ABC, abstractmethod
from typing import Any
from src.domain.models import WeatherReport

class Client(ABC):
    """Универсальный HTTP-клиент"""
    @abstractmethod
    async def make_request(self, request: Any) -> Any:
        pass

class WeatherFetcher(ABC):
    @abstractmethod
    async def fetch_weather(self, city: str) -> WeatherReport:
        pass

class Exporter(ABC):
    @abstractmethod
    def export(self, report: WeatherReport) -> str:
        pass

class LogRepository(ABC):
    @abstractmethod
    def log_request(self, city: str, success: bool, error: str = "") -> None:
        pass