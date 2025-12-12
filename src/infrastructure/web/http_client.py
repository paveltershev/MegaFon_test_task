import httpx
from src.domain.interfaces import Client

class HttpClient(Client):
    async def make_request(self, request: dict) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=request["url"],
                headers=request.get("headers", {}),
                timeout=request.get("timeout", 10)
            )
            response.raise_for_status()
            return response.json()  # или response.text, если HTML, вероятно лучше переписать на конструкцию if json/html
