from integrador.informezz.settings import BASE_URL
import requests

class LojaClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def obter_dados(self):
        headers = {
            "x-api-key": self.api_key
        }

        url = f"{BASE_URL}/store"
        response = requests.get(url, headers=headers)

        response.raise_for_status()
        return response.json()
