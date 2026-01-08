from integrador.ssotica.settings import BASE_URL
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

class EstoqueClient:
    def __init__(self, token: str, empresa: str):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        self.params = {
            "empresa": empresa
        }
        self.session = requests.Session()
        self.max_workers = 30

    def _fetch_page(self, page):
        url = f"{BASE_URL}/produto/estoque/busca?page={page}"
        response = self.session.get(url, headers=self.headers, params=self.params)
        response.raise_for_status()
        payload = response.json()

        return {
            "page": page,
            "totalpages": payload["totalPages"],
            "data": payload["data"],
        }

    def obter_dados(self):
        current_page = 1

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while True:
                futures = {
                    executor.submit(self._fetch_page, p): p
                    for p in range(current_page, current_page + self.max_workers)
                }

                page_results = []
                for future in as_completed(futures):
                    result = future.result()
                    page_results.append(result)

                page_results.sort(key=lambda x: x["page"])

                for res in page_results:
                    yield res["data"]
                    if current_page >= res["totalpages"]:
                        return

                current_page += self.max_workers