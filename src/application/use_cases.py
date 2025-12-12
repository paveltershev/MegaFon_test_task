from src.domain.interfaces import WeatherFetcher, Client, Exporter, LogRepository
from src.domain.models import WeatherReport
from src.infrastructure.web.yandex_mapper import YandexResponseMapper


class WeatherParsingUseCase(WeatherFetcher):
    def __init__(
            self,
            http_client: Client,
            exporter: Exporter,
            log_repo: LogRepository
    ):
        self._client = http_client
        self._exporter = exporter
        self._log_repo = log_repo
        self._mapper = YandexResponseMapper()

    async def fetch_weather(self, city: str) -> WeatherReport:
        request = self._build_request(city)
        raw_response = await self._client.make_request(request)
        report = self._mapper.to_weather_report(raw_response, city)
        return report

    def _build_request(self, city: str) -> dict:
        return {
            "url": f"https://yandex.ru/weather/?city={city}",
            "headers": {"User-Agent": "Mozilla/5.0"},
            "timeout": 10,
        }

    async def execute(self, city: str) -> str:
        """Полный сценарий: fetch → export → log"""
        try:
            report = await self.fetch_weather(city)
            filename = self._exporter.export(report)
            self._log_repo.log_request(city, success=True)
            return filename
        except Exception as e:
            self._log_repo.log_request(city, success=False, error=str(e))
            raise