import requests
import json

from typing import Union, Tuple, List, Any, Dict

from rest_framework.views import Request

from .BaseRequester import BaseRequester, CustomCurcuitBreaker
from .TokenRequester import TokenRequester
from ..decorators import TokenHeader

from django.core.cache import cache
from django.conf import settings

PublisherCB = CustomCurcuitBreaker()
PTReq = TokenRequester(service = 'PUBLISHER')
PID, PSECRET = settings.PUBLISHER_CREDENTIALS['id'], settings.PUBLISHER_CREDENTIALS['secret']

class PublisherRequester(BaseRequester):
    TOKENS = {
        'html' : 'html/',
        'publisher' : 'publisher/'
    }

    URL = ''

    def __init__(self):
        self.URL = self.URLS['PUBLISHER']

    def __user_exists(self, request: Request, u_id: int) -> bool:
        from api.requesters.UserRequester import UserRequester

        _, code = UserRequester().user(request = request, id_ = u_id)

        return code == 200

    def __user_by_token(self, request: Request) -> Tuple[Dict[str, str], int]:
        from api.requesters.UserRequester import UserRequester

        u_json, code = UserRequester().info(request = request)

        return u_json, code

    @PublisherCB
    @TokenHeader(cache = cache, requester = PTReq, app_id = PID, app_secret = PSECRET, t_label = 'publisher-token')
    def publishers(self, request: Request, headers: dict = {}) -> Tuple[Dict[str, str], int]:
        url = self.URL

        # u_json, code = self.__user_by_token(request)

        # if code != 200:
        #     return (u_json, code)

        # url += f'?user_id={u_json["id"]}'

        limitoffset = self._limit_offset_from_request(request)

        if limitoffset:
            url += f'&limit={limitoffset[0]}&offset={limitoffset[1]}'

        response = self.get(
            url = url,
            headers = headers
        )

        response_json, code = self._process_response(
            response = response,
            task_name = 'PUBLISHERS'
        )

        response_json = self._safe_next_previous_link(
            response = response
        )

        return (response_json, response.status_code)

    @PublisherCB
    @TokenHeader(cache = cache, requester = PTReq, app_id = PID, app_secret = PSECRET, t_label = 'publisher-token')
    def publisher(self, request: Request, uuid: str, headers: dict = {}) -> Tuple[Dict[str, str], int]:
        response = self.get(
            url = self.URL + f'{uuid}/',
            headers = headers
        )

        return self._process_response(
            response = response,
            task_name = 'PUBLISHER'
        )

    @PublisherCB
    @TokenHeader(cache = cache, requester = PTReq, app_id = PID, app_secret = PSECRET, t_label = 'publisher-token')
    def post_publisher(self, request: Request, data: dict, headers: dict = {}) -> Tuple[dict, int]:
        # check request and data

        response = self.post(
            url = self.URL,
            data = data,
            headers = headers
        )

        return self._process_response(
            response = response,
            task_name = 'POST_PUBLISHER'
        )

    @PublisherCB
    @TokenHeader(cache = cache, requester = PTReq, app_id = PID, app_secret = PSECRET, t_label = 'publisher-token')
    def patch_publisher(self, request: Request, data: dict, uuid: str, headers: dict = {}) -> Tuple[Dict[str, str], int]:
        # check request and data

        response = self.patch(
            url = self.URL + f'{uuid}/',
            data = data,
            headers = headers
        )

        return response._process_response(
            response = response,
            task_name = 'PATCH_PUBLISHER'
        )

    @PublisherCB
    @TokenHeader(cache = cache, requester = PTReq, app_id = PID, app_secret = PSECRET, t_label = 'publisher-token')
    def delete_publisher(self, request: Request, data: dict, uuid: str, headers: dict = {}) -> Tuple[Dict[str, str], int]:
        publisher_json, code = self.publisher(request, uuid)

        if code != 200:
            return publisher_json, code

        response = self.delete(
            url = self.URL + f'{uuid}/',
            data = data,
            headers = headers
        )

        return response._process_response(
            response = response,
            task_name = 'DELETE_PUBLISHER'
        )
