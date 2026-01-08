from integrador.ssotica.settings import BASE_URL
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import timedelta
from django.utils import timezone

class VendaClient:
    def __init__(self, token: str, cnpj: str):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        self.url = f"{BASE_URL}/integracoes/vendas/periodo"
        self.cnpj = cnpj
        self.session = requests.Session()
        self.max_workers = 30

    def _fetch_page(self, start_date, end_date):
        params = {
            "cnpj": self.cnpj,
            "inicio_periodo": start_date,
            "fim_periodo": end_date,
        }

        response = self.session.get(self.url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def obter_dados(self, start_date):
        window_size = 30
        current_start = start_date
        now = timezone.now().date()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while current_start <= now:

                # 1) Montar janelas futuras (até max_workers)
                windows = []
                for i in range(self.max_workers):
                    win_start = current_start + timedelta(days=i * window_size)
                    if win_start > now:
                        break

                    win_end = min(
                        win_start + timedelta(days=window_size - 1),
                        now
                    )
                    windows.append((win_start, win_end))

                # 2) Disparar requisições em paralelo
                futures = {
                    executor.submit(self._fetch_page, start, end): start
                    for start, end in windows
                }

                # 3) Coletar resultados
                results = []
                for future in as_completed(futures):
                    data = future.result()
                    results.append({
                        "start": futures[future],
                        "data": data
                    })

                # 4) Ordenar por data de início
                results.sort(key=lambda x: x["start"])

                # 5) Entregar dados ao importer
                for res in results:
                    yield res["data"]

                # 6) Avançar para o próximo bloco
                current_start = windows[-1][1] + timedelta(days=1)