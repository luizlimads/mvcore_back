from integrador.informezz.settings import BASE_URL
import requests
from django.utils import timezone

class EstoqueClient:
    def __init__(self, api_key: str, timeout: int = 30):
        self.headers = {"x-api-key": api_key}
        self.url = f"{BASE_URL}/stock"
        self.timeout = timeout
        self.session = requests.Session()

    def _fetch_page(self, start_date, page: int, pagesize: int = 50) -> dict:
        params = {
            "startdate": start_date,
            "enddate": timezone.now().date(),
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
    
    def obter_dados(self, start_date, page_start, page_end):
        page = page_start

        if page_end is None:
            page_end = self.obter_total_paginas()

        while page <= page_end:
            payload = self._fetch_page(start_date, page)

            data = payload.get("data", [])

            if data:
                yield data

            page += 1

    def obter_total_paginas(self, start_date):
        payload = self._fetch_page(start_date, 1)
        return payload.get("totalPages", 1)