import base64
import hashlib
import json
import urllib
from urllib.parse import urljoin

import aiohttp


class LiqPay:
    def __init__(self,
                 private_key: str,
                 public_key: str,
                 client_server: str = "request",
                 server_server: str = "3/checkout"
                 ):
        self.private_key = private_key
        self.public_key = public_key
        self.host = "https://www.liqpay.ua/api/"
        self.client_server = client_server
        self.server_server = server_server

    STATUS_MAPPING = {
        'error': 0,
        'failure': 1,
        'reversed': 2,
        'success': 3,
        'hold_wait': 4,
    }

    @classmethod
    def headers(cls):
        return {
            'Content-Type': 'application/json'
        }

    def __generate_signature(self, data: dict) -> tuple[str, str]:
        string_data = json.dumps(data)
        encoded_data = base64.b64encode(string_data.encode('utf-8')).decode('utf-8')
        signature = base64.b64encode(
            hashlib.sha1((self.private_key + encoded_data + self.private_key).encode('utf-8')).digest()).decode('utf-8')
        return encoded_data, signature

    async def post(self, data: dict, return_url: bool = False) -> dict:
        data.update(public_key=self.public_key)

        json_encoded_data, signature = self.__generate_signature(data)
        request_data = {"data": json_encoded_data, "signature": signature}
        request_data = urllib.parse.urlencode(request_data)

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    urljoin(self.host, self.client_server if not return_url else self.server_server),
                    data=request_data,
                    headers=self.headers()
                ) as resp:
                    if return_url:
                        return {"url": str(resp.url),
                                "status": self.STATUS_MAPPING.get("hold_wait")}

                    response_data = await resp.json()
                    response_data.update({
                        "status": self.STATUS_MAPPING.get(response_data.get("status"), 0)
                    })

                    return response_data

            except aiohttp.ClientError:
                return {"status": self.STATUS_MAPPING.get("error")}
