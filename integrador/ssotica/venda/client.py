from integrador.ssotica.settings import BASE_URL
import requests
from datetime import timedelta
from django.utils import timezone

class VendaClient:
    def __init__(self, token: str, cnpj: str, timeout: int = 30):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        self.url = f"{BASE_URL}/integracoes/vendas/periodo"
        self.cnpj = cnpj
        self.timeout = timeout
        self.session = requests.Session()

    def _fetch_periodo(self, start_date, end_date):
        params = {
            "cnpj": self.cnpj,
            "inicio_periodo": start_date,
            "fim_periodo": end_date,
        }

        response = self.session.get(self.url, headers=self.headers, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def obter_dados(self, start_date, window_size=30):
        current_start = start_date
        now = timezone.now().date()

        while current_start <= now:
            current_end = min(
                current_start + timedelta(days=window_size - 1),
                now
            )

            data = self._fetch_periodo(current_start, current_end)

            if data:
                yield data

            current_start = current_end + timedelta(days=1)
