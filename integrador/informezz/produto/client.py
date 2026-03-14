from integrador.informezz.settings import BASE_URL
import requests

class ProdutoClient:
    def __init__(self, api_key: str, timeout: int = 30):
        self.headers = {"x-api-key": api_key}
        self.url = f"{BASE_URL}/product"
        self.timeout = timeout
        self.session = requests.Session()

    def _fetch_page(self, page: int, pagesize: int = 50) -> dict:
        params = {
            "pagination.pagenumber": page,
            "pagination.pagesize": pagesize,
        }

        response = self.session.get(self.url, headers=self.headers, params=params, timeout=self.timeout)
        response.raise_for_status()
        payload = response.json()

        return {
            "data": payload["data"],
            "totalPages": payload["metadata"]["totalPages"],
        }

    def obter_dados(self, page_start, page_end):
        page = page_start

        if page_end is None:
            page_end = self.obter_total_paginas()

        while page <= page_end:
            payload = self._fetch_page(page)
            data = payload.get("data", [])

            if data:
                yield data

            page += 1

    def obter_total_paginas(self):
        payload = self._fetch_page(1)
        return payload.get("totalPages", 1)

