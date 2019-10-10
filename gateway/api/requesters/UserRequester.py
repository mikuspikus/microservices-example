import requests
from typing import Union, Tuple, List, Any, Dict

from gateway.settings import DEBUG
from .BaseRequester import BaseRequester

from rest_framework.views import Request

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