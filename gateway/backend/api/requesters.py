import requests
import json

from typing import Union, Tuple, List, Any, Dict

from gateway.settings import DEBUG

from logging import Logger

from rest_framework.views import Request

class BaseRequester():
    logger = Logger(name = 'Requester Logger')

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

    def __token(self, request: Request) -> str:
        token = request.META['HTTP_AUTHORIZATION']
        token = token[6:]

        return token

    def authenticate_header(self, request: Request) -> Union[Dict[str, str], None]:
        try:
            return {'Authentication' : f'Token {self.__token(request)}'}

        except KeyError:
            return None

class UserRequester(BaseRequester):
    TOKENS = {
        'auth' : 'auth/',
        'register' : 'register/',
        'info' : 'info/',
        'users' : 'users/',
    }
    URL = ''

    def __init__(self):
        self.URL = self.URLS['USER']

    def __logging(self, response: requests.Response, task_name: str) -> Tuple[Dict[str, str], int]:
        '''
        '''
        if response is None:
            return {}, 504

        try:
            self.logger.info('{task_name} {code}', task_name, response.status_code)
            return response.json(), response.status_code

        except ValueError as error:
            self.logger.exception('{method_name} {message}', task_name, error.msg)

        return response.text, response.status_code

    def authenticate(self, data: dict) -> Tuple[Dict[str, str], int]:
        response = self.post(
            url = self.URL + self.TOKENS['auth'],
            data = data
        )

        return self.__logging(response = response, task_name = 'AUTHENTICATE')

    def register(self, data: dict) -> Tuple[Dict, int]:
        response = self.post(
            url = self.URL + self.TOKENS['register'],
            data = data
        )

        return self.__logging(response = response, task_name = 'REGISTER')

    def info(self, request: Request) -> Tuple[Dict, int]:
        response = self.get(
            url = self.URL + self.TOKENS['info'],
            headers = self.authenticate_header(request),
        )

        return self.__logging(response = response, task_name = 'INFO')

    def users(self, request: Request, limit_offset: (int, int) = None) -> Tuple[Dict, int]:
        url = self.URL + self.TOKENS['users']

        if limit_offset:
            url += f'?limit={limit_offset[0]}&offset={limit_offset[1]}'

        response = self.get(
            url = url,
            headers = self.authenticate_header(request),
        )

        return self.__logging(response = response, task_name = 'USERS')

    def user(self, request: Request, id_: int) -> Tuple[Dict, int]:
        response = self.get(
            url = self.URL + self.TOKENS['users'] + f'{id_}/',
            headers = self.authenticate_header(request),
        )

        return self.__logging(response = response, task_name = 'USER')

    def delete(self, request: Request) -> Tuple[Dict, int]:
        info_json, code = self.info(token  = token)

        if code != 200:
            return info_json, code

        '''
        TODO: delete user stuff (delete uuid from articles)
        '''
        id_ = info_json['id']

        response = self.delete(
            url = self.URL + self.TOKENS['info'],
            headers = self.authenticate_header(request),
        )

        return self.__logging(response = response, task_name = 'DELETE')


class ArticleRequester(BaseRequester):
    TOKENS = {

    }

    URL = ''

    def __init__(self):
        self.URL = self.URLS['ARTICLE']
