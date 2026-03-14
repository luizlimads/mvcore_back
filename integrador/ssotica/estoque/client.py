from integrador.ssotica.settings import BASE_URL
import requests

class EstoqueClient:
    def __init__(self, token: str, empresa: str, timeout: int = 30):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        self.params = {
            "empresa": empresa
        }
        self.timeout = timeout
        self.session = requests.Session()

    def _fetch_page(self, page: int) -> dict:
        url = f"{BASE_URL}/produto/estoque/busca?page={page}"
        response = self.session.get(url, headers=self.headers, params=self.params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def obter_dados(self):
        page = 1

        while True:
            payload = self._fetch_page(page)

            data = payload.get("data", [])
            total_pages = payload.get("totalPages", 1)

            if data:
                yield data

            if page >= total_pages:
                return

            page += 1
