import requests
import json
import logging
import re

from typing import Union, Tuple, List, Any, Dict

from ...gateway.settings import DEBUG

from rest_framework.views import Request

class BaseRequester():
    logger = logging.getLogger(name = 'requester')

    URLS = {
        'USER' : 'http://localhost:8081/auth/' if DEBUG else '',
        'ARTICLE' : 'http://localhost:8082/article/' if DEBUG else '',
        'JOURNAL' : 'http://localhost:8083/journal/' if DEBUG else '',
        'PUBLISHER' : 'http://localhost:8084/publisher/' if DEBUG else '',
    }

    TOKENS = {}

    def get(self, url: str, headers: dict = {}) -> Union[requests.Response, None]:
        try:
            self.logger.info('{request_type} {url} {headers}', 'GET', url, headers)
            response = requests.get(url = url, headers = headers)

        except requests.exceptions.RequestException as error:
            self.logger.exception('{request_type} {url} {headers} {message}', 'GET', url, headers, str(error))
            return None

        return response

    def post(self, url: str, data: dict = {}, headers: dict = {}) -> Union[requests.Response, None]:
        try:
            self.logger.info('{request_type} {url} {headers}', 'POST', url, headers)
            response = requests.post(url = url, json = data, headers = headers)

        except requests.exceptions.RequestException as error:
            self.logger.exception('{request_type} {url} {headers} {message}', 'POST', url, headers, str(error))
            return None

        return response

    def delete(self, url: str, headers: dict = {}) -> Union[requests.Response, None]:
        try:
            self.logger.info('{request_type} {url} {headers}', 'DELETE', url, headers)
            response = requests.delete(url = url, headers = headers)

        except requests.exceptions.RequestException as error:
            self.logger.exception('{request_type} {url} {headers} {message}', 'DELETE', url, headers, str(error))
            return None

        return response

    def patch(self, url: str, data: dict = {}, headers: dict = {}) -> Union[requests.Response, None]:
        try:
            self.logger.info('{request_type} {url} {headers}', 'PATCH', url, headers)
            response = requests.patch(url = url, json = data, headers = headers)

        except requests.exceptions.RequestException as error:
            self.logger.exception('{request_type} {url} {headers} {message}', 'PATCH', url, headers, str(error))
            return None

        return response

    def put(self, url: str, data: dict = {}, headers: dict = {}) -> Union[requests.Response, None]:
        try:
            self.logger.info('{request_type} {url} {headers}', 'PUT', url, headers)
            response = requests.put(url = url, json = data, headers = headers)

        except requests.exceptions.RequestException as error:
            self.logger.exception('{request_type} {url} {headers} {message}', 'PUT', url, headers, str(error))
            return None

        return response

    def __token_from_request(self, request: Request) -> str:
        '''
        Raises KeyError
        '''
        token = request.META['HTTP_AUTHORIZATION']
        token = token[6:]

        return token

    def authenticate_header(self, request: Request) -> Union[Dict[str, str], None]:
        try:
            return {'Authentication' : f'Token {self.__token(request)}'}

        except KeyError:
            return None

    def __limit_offset_from_request(self, request: Request) -> Union[Tuple[int, int], None]:
        try:
            limit = request.query_params['limit']
            offset = request.query_params['offset']
        
        except KeyError:
            return None

        return (limit, offset)

    def __limit_offset_from_link(self, link: str) -> Union[Tuple[int, int], None]:
        str_limit, str_offset = re.findall(r'limit=\d+', link), re.findall(r'offset=\d+', link)

        limit = int(re.findall(r'\d+', str_limit[0])) if len(str_limit) else 0
        offset = int(re.findall(r'\d+', str_offset[0])) if len(str_offset) else 0

        return (limit, offset)

    def __next_previous_link(self, data: dict) -> Dict[str, str]:
        try:
            next_link, previous_link = data['next'], data['previous']

        except KeyError:
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

    def __process_response(self, response: requests.Response, task_name: str) -> Tuple[Dict[str, str], int]:
        '''
        '''
        if response is None:
            return ({'errors' : f'no valid response from {response.url}'}, 504)

        try:
            self.logger.info('{task_name} {code}', task_name, response.status_code)
            return response.json(), response.status_code

        except ValueError as error:
            self.logger.exception('{method_name} {message}', task_name, error.msg)
            return response.text, response.status_code