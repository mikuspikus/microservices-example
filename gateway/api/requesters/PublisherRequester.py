import requests
import json

from typing import Union, Tuple, List, Any, Dict

from rest_framework.views import Request

from .BaseRequester import BaseRequester

class PublisherRequester(BaseRequester):
    TOKENS = {

    }

    URL = ''

    def __init__(self):
        self.URL = self.URLS['PUBLISHER']

    def publishers(self, request: Request) -> Tuple[Dict[str, str], int]:
        url = self.URL

        u_json, code = self.__user_by_token(request)

        if code != 200:
            return (u_json, code)

        url += f'?user_id={u_json["id"]}'

        limitoffset = self.__limit_offset_from_request(request)

        if limitoffset:
            url += f'&limit={limitoffset[0]}&offset={limitoffset[1]}'

        response_json, code = response = self.get(
            url = url,
        )

        self.__process_response(
            response = response,
            task_name = 'PUBLISHERS'
        )

        response_json = self.__next_previous_link(
            data = response.json()
        )

        return (response_json, response.status_code)

    def publisher(self, request: Request, uuid: str) -> Tuple[Dict[str, str], int]:
        response = self.get(
            url = self.URL + f'{uuid}/'
        )

        return self.__process_response(
            response = response,
            task_name = 'PUBLISHER'
        )

    def post_publisher(self, request: Request, data: dict) -> Tuple[dict, int]:
        # check request and data

        response = self.post(
            url = self.URL,
            data = data
        )

        return response.__process_response(
            response = response,
            task_name = 'POST_PUBLISHER'
        )

    def patch_publisher(self, request: Request, data: dict, uuid: str) -> Tuple[Dict[str, str], int]:
        # check request and data

        response = self.patch(
            url = self.URL + f'{uuid}/',
            data = data
        )

        return response.__process_response(
            response = response,
            task_name = 'PATCH_ARTICLE'
        )

    def delete_publisher(self, request: Request, data: dict, uuid: str) -> Tuple[Dict[str, str], int]:
        publisher_json, code = self.publisher(request, uuid)

        if code != 200:
            return publisher_json, code

        response = self.delete(
            url = self.URL + f'{uuid}/',
            data = data
        )

        return response.__process_response(
            response = response,
            task_name = 'DELETE_PUBLISHER'
        )
