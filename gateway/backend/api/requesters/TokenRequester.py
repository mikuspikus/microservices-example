
from .BaseRequester import BaseRequester
from requests.exceptions import RequestException

class TokenRequester(BaseRequester):
    TOKENS = {
        'AUTH': 'auth/'
    }

    def __init__(self, service: str):
        self.URL = self.URLS[service]

    def token(self, app_id, app_secret):
        self.loginfo(f'requesting token for {self.URL}')

        response = self.post(
            url = f'{self.URL}{self.TOKENS["AUTH"]}',
            data = {'app_id': app_id, 'app_secret': app_secret}
        )

        json, code = self._process_response(
            response = response,
            task_name = 'REQUEST-TOKEN'
        )

        return (json, code)
