from api.requesters.BaseRequester import BaseRequester

from typing import Tuple, Dict

from requests.exceptions import RequestException

class JobRequester(BaseRequester):
    URL = ''

    def __init__(self):
        self.URL = self.URLS['PUBLISHER']

    def post(self, payload: dict) -> int:
        data, headers = payload['data'], payload['headers']

        response = super().post(url = self.URL, data = data, headers = headers)
        return response.status_code

    def delete(self, payload: dict) -> int:
        uuid, headers = payload['uuid'], payload['headers']

        response = super().delete(url = f'{self.URL}{uuid}/', headers = headers)
        return response.status_code


    def patch(self, payload: dict) -> int:
        uuid, data, headers = payload['uuid'], payload['data'], payload['headers']

        response = super().patch(url = f'{self.URL}{uuid}/', data = data, headers = headers)
        return response.status_code
