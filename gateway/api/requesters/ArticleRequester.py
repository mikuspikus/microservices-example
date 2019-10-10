import requests
import json
from logging import Logger
from typing import Union, Tuple, List, Any, Dict

from gateway.settings import DEBUG

from rest_framework.views import Request

from .BaseRequester import BaseRequester

class ArticleRequester(BaseRequester):
    TOKENS = {

    }

    URL = ''

    def __init__(self):
        self.URL = self.URLS['ARTICLE']

    def __user_exists(self, request: Request, u_id: int) -> bool:
        from api.requesters.UserRequester import UserRequester

        _, code = UserRequester().user(request = request, id_ = u_id)

        return code == 200

    def __user_by_token(self, request: Request) -> Tuple[Dict[str, str], int]:
        from api.requesters.UserRequester import UserRequester

        u_json, code = UserRequester().info(request = request)

        return u_json, code

    def articles(self, request: Request) -> Tuple[Dict[str, str], int]:
        url = self.URL

        u_json, code = self.__user_by_token(request)

        if code != 200:
            return (u_json, code)

        url += f'?user_id={u_json["id"]}'

        limitoffset = self.__limit_offset_from_request(request)

        if limitoffset:
            url += f'&limit={limitoffset[0]}&offset={limitoffset[1]}'

        response = self.get(
            url = url,
        )

        response_json, code = self.__process_response(
            response = response,
            task_name = 'ARTICLES'
        )

        response_json = self.__next_previous_link(
            data = response.json()
        )

        return (response_json, code)

    def article(self, request: Request, uuid: str) -> Tuple[Dict[str, str], int]:
        response = self.get(
            url = self.URL + f'{uuid}/'
        )

        return self.__process_response(
            response = response,
            task_name = 'ARTICLE'
        )

    def post_article(self, request: Request, data: dict) -> Tuple[Dict[str, str], int]:
        # check request and data

        response = self.post(
            url = self.URL,
            data = data
        )

        return response.__process_response(
            response = response,
            task_name = 'POST_ARTICLE'
        )

    def patch_article(self, request: Request, data: dict, uuid: str) -> Tuple[Dict[str, str], int]:
        # check request and data

        response = self.patch(
            url = self.URL + f'{uuid}/',
            data = data
        )

        return response.__process_response(
            response = response,
            task_name = 'PATCH_ARTICLE'
        )

    def delete_article(self, request: Request, data: dict, srt_uuid: str) -> Tuple[Dict[str, str], int]:
        article_json, code = self.article(request, uuid)

        if code != 200:
            return article_json, code

        response = self.delete(
            url = self.URL + f'{uuid}/',
            data = data
        )

        return response.__process_response(
            response = response,
            task_name = 'DELETE_ARTICLE'
        )
