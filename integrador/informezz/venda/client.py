from integrador.informezz.settings import BASE_URL
from django.utils import timezone
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

class VendaClient:
    def __init__(self, api_key):
        self.headers = {"x-api-key": api_key}
        self.url = f"{BASE_URL}/sale"
        self.session = requests.Session()
        self.max_workers = 30

    def _fetch_page(self, page, start_date):
        params = {
            "startdate": start_date,
            "enddate":  timezone.now().date().strftime("%Y-%m-%d"),
            "pagination.pagenumber": page,
            "pagination.pagesize": 50,
        }

        response = self.session.get(self.url, headers=self.headers, params=params)
        response.raise_for_status()
        payload = response.json()

        return {
            "page": page,
            "data": payload["data"],
            "hasNext": payload["metadata"]["hasNext"],
        }

    def obter_dados(self, start_date):
        current_page = 1
        has_next = True

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while has_next:

                futures = {
                    executor.submit(self._fetch_page, p, start_date): p
                    for p in range(current_page, current_page + self.max_workers)
                }

                page_results = []
                for future in as_completed(futures):
                    result = future.result()
                    page_results.append(result)

                page_results.sort(key=lambda x: x["page"])

                for res in page_results:
                    yield res["data"]
                    if not res["hasNext"]:
                        return

                current_page += self.max_workers
