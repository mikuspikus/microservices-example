import requests
import json

from typing import Union, Tuple, List, Any, Dict

from rest_framework.views import Request

from .BaseRequester import BaseRequester, CustomCurcuitBreaker

PublisherCB = CustomCurcuitBreaker()

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
    def publishers(self, request: Request) -> Tuple[Dict[str, str], int]:
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
    def publisher(self, request: Request, uuid: str) -> Tuple[Dict[str, str], int]:
        response = self.get(
            url = self.URL + f'{uuid}/'
        )

        return self._process_response(
            response = response,
            task_name = 'PUBLISHER'
        )

    @PublisherCB
    def post_publisher(self, request: Request, data: dict) -> Tuple[dict, int]:
        # check request and data

        response = self.post(
            url = self.URL,
            data = data
        )

        return self._process_response(
            response = response,
            task_name = 'POST_PUBLISHER'
        )

    @PublisherCB
    def patch_publisher(self, request: Request, data: dict, uuid: str) -> Tuple[Dict[str, str], int]:
        # check request and data

        response = self.patch(
            url = self.URL + f'{uuid}/',
            data = data
        )

        return response._process_response(
            response = response,
            task_name = 'PATCH_PUBLISHER'
        )

    @PublisherCB
    def delete_publisher(self, request: Request, data: dict, uuid: str) -> Tuple[Dict[str, str], int]:
        publisher_json, code = self.publisher(request, uuid)

        if code != 200:
            return publisher_json, code

        response = self.delete(
            url = self.URL + f'{uuid}/',
            data = data
        )

        return response._process_response(
            response = response,
            task_name = 'DELETE_PUBLISHER'
        )
