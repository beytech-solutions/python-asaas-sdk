import requests

from asaas.http import BaseAPIRequest

class NewPayment(BaseAPIRequest):
    def call(self, base_url: str, headers: dict, data: dict) -> requests.Response:
        data = kwargs.pop("data", {})
        
        return requests.post(
            f"{base_url}/payments",
            headers=headers,
            json=data
        )