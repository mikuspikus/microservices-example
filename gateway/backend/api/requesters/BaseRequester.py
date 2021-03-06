import requests
import json
import logging
import re
from circuitbreaker import CircuitBreaker

from typing import Union, Tuple, List, Any, Dict

# from django.conf import settings
DEBUG = True #settings.DEBUG

# from rest_framework.views import Request, Response

class CustomCurcuitBreaker(CircuitBreaker):
    FAILURE_THRESHOLD = 5
    RECOVERY_TIMEOUT = 60
    EXPECTED_EXCEPTION = requests.exceptions.RequestException

class BaseRequester():
    logger = logging.getLogger(name = 'api.requester')
    formatter = '{msg}'

    URLS = {
        'USER' : 'http://localhost:8081/user/' if DEBUG else '',
        'ARTICLE' : 'http://localhost:8082/articles/' if DEBUG else '',
        'JOURNAL' : 'http://localhost:8083/journals/' if DEBUG else '',
        'PUBLISHER' : 'http://localhost:8084/publishers/' if DEBUG else '',
    }

    TOKENS = {}

    def loginfo(self, msg: str = None) -> None:
        self.logger.info(
            self.formatter.format(
                msg = msg
            )
        )

    def logexception(self, msg: str = None) -> None:
        self.logger.exception(
            self.formatter.format(
                msg = msg
            )
        )

    def get(self, url: str, headers: dict = {}) -> Union[requests.Response, None]:
        self.loginfo(
            msg = '{request_type} {url} {headers}'.format(
            request_type = 'GET', 
            url = url, 
            headers = headers
            )
        )

        return requests.get(url = url, headers = headers)

    def post(self, url: str, data: dict = {}, headers: dict = {}) -> Union[requests.Response, None]:
        self.loginfo(
            msg = '{request_type} {url} {headers}'.format(
                request_type = 'POST', 
                url = url, 
                headers = headers
            )
        )
        return requests.post(url = url, json = data, headers = headers)

    def delete(self, url: str, headers: dict = {}) -> Union[requests.Response, None]:
        self.loginfo(
            msg = '{request_type} {url} {headers}'.format(
                request_type = 'DELETE', 
                url = url, 
                headers = headers
            )
        )
        return requests.delete(url = url, headers = headers)

    def patch(self, url: str, data: dict = {}, headers: dict = {}) -> Union[requests.Response, None]:
        self.loginfo(
            msg = '{request_type} {url} {headers}'.format(
                request_type = 'PATCH', 
                url = url, 
                headers = headers
            )
        )
        return requests.patch(url = url, json = data, headers = headers)

    def put(self, url: str, data: dict = {}, headers: dict = {}) -> Union[requests.Response, None]:
        self.loginfo(
            msg = '{request_type} {url} {headers}'.format(
                request_type = 'PUT', 
                url = url, 
                headers = headers
            )
        )
        return requests.put(url = url, json = data, headers = headers)

    def _token_from_request(self, request) -> str:
        '''
        Raises KeyError
        '''
        token = request.META['HTTP_AUTHORIZATION']
        return token

    def authenticate_header(self, request) -> Union[Dict[str, str], None]:
        try:
            return {'Authorization' : f'Bearer {self._token_from_request(request)}'}

        except KeyError:
            return None

    def _limit_offset_from_request(self, request) -> Union[Tuple[int, int], None]:
        try:
            limit = request.query_params['limit']
            offset = request.query_params['offset']
        
        except KeyError:
            return None

        return (limit, offset)

    def _limit_offset_from_link(self, link: str) -> Union[Tuple[int, int], None]:
        str_limit, str_offset = re.findall(r'limit=\d+', link), re.findall(r'offset=\d+', link)

        limit = int(re.findall(r'\d+', str_limit[0])) if len(str_limit) else 0
        offset = int(re.findall(r'\d+', str_offset[0])) if len(str_offset) else 0

        return (limit, offset)

    def _next_previous_link(self, data: dict) -> Dict[str, str]:
        try:
            next_link, previous_link = data['next'], data['previous']

        except (KeyError, TypeError):
            return data

        if next_link:
            try:
                limit, offset = self.__limit_offset_from_link(next_link)

            except ValueError:
                limit, offset = 0, 0

            data['next'] = f'?limit={limit}&offset={offset}'

        if previous_link:
            try:
                limit, offset = self.__limit_offset_from_link(previous_link)

            except ValueError:
                limit, offset = 0, 0

            data['previous'] = f'?limit={limit}&offset={offset}'

        return data

    def _safe_next_previous_link(self, response):
        try:
            return self._next_previous_link(
                data = response.json()
            )

        except ValueError:
            return response.text

    def _process_response(self, response: requests.Response, task_name: str) -> Tuple[Union[Dict[str, str], str], int]:
        '''
        '''
        if response is None:
            self.loginfo(
                msg = f'no valid response'
            )
            return ({'errors' : f'no valid response'}, 504)

        try:
            self.loginfo(
                msg = '{task_name} {code}'.format(
                    task_name = task_name, 
                    code = response.status_code
                )
            )
            return response.json(), response.status_code

        except ValueError as error:
            self.logexception(
                msg = '{task_name} {code}'.format(
                    task_name = task_name, 
                    code = response.status_code
                )
            )
            return response.text, response.status_code