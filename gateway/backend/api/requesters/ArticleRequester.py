import requests
import json
from logging import Logger
from typing import Union, Tuple, List, Any, Dict

from gateway.settings import DEBUG

from rest_framework.views import Request, status

from .BaseRequester import BaseRequester
from .PublisherRequester import PublisherRequester
from .JournalRequester import JournalRequester

class ArticleError(Exception):
    pass

class ArticleRequester(BaseRequester):
    TOKENS = {

    }

    URL = ''

    journal_requester = JournalRequester()

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

    def user_articles(self, request: Request, **kwargs):
        url = self.URL

        if kwargs:
            url = url[:-1] + '?' + '&'.join(
                [
                    f'{arg}={value}' for arg, value in kwargs.items()
                ]
            )

        response = self.get(
            url = url,
        )

        response_json, code = self._process_response(
            response = response,
            task_name = 'USER_ARTICLES'
        )

        return (response_json, code)

    def articles(self, request: Request) -> Tuple[Dict[str, str], int]:
        url = self.URL

        '''
        u_json, code = self.__user_by_token(request)

        if code != 200:
            return (u_json, code)

        url += f'?author={u_json["outer_uuid"]}'

        '''
        limitoffset = self._limit_offset_from_request(request)

        if limitoffset:
            url += f'&limit={limitoffset[0]}&offset={limitoffset[1]}'

        response = self.get(
            url = url,
        )

        response_json, code = self._process_response(
            response = response,
            task_name = 'ARTICLES'
        )

        try:
            response_json = self._next_previous_link(
                data = response.json()
            )

        except AttributeError as error:
            pass

        return (response_json, code)

    def article(self, request: Request, uuid: str) -> Tuple[Dict[str, str], int]:
        response = self.get(
            url = self.URL + f'{uuid}/'
        )

        return self._process_response(
            response = response,
            task_name = 'ARTICLE'
        )

    def post_article(self, request: Request, data: dict) -> Tuple[Dict[str, str], int]:
        try:
            is_article_valid = self.check_article(request, data)

        except ArticleError as error:
            return ({'errors' : str(error)}, status.HTTP_400_BAD_REQUEST)

        if not is_article_valid:
            return ({'errors' : 'journal not found'}, status.HTTP_404_NOT_FOUND)

        response = self.post(
            url = self.URL,
            data = data
        )

        return self._process_response(
            response = response,
            task_name = 'POST_ARTICLE'
        )

    def patch_article(self, request: Request, data: dict, uuid: str) -> Tuple[Dict[str, str], int]:
        try:
            is_article_valid = self.check_article(request, data)

        except ArticleError as error:
            return ({'errors' : str(error)}, status.HTTP_400_BAD_REQUEST)

        if not is_article_valid:
            return ({'errors' : 'journal not found'}, status.HTTP_404_NOT_FOUND)

        response = self.patch(
            url = self.URL + f'{uuid}/',
            data = data
        )

        return response._process_response(
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

        return response._process_response(
            response = response,
            task_name = 'DELETE_ARTICLE'
        )


    def journals_exists(self, request: Request, j_uuid: str) -> bool:
        self.loginfo(
            '{task_name} {msg}'.format(
                task_name = 'JOURNAL_EXISTS',
                msg = f'checking with j_uuid = {j_uuid}'
            )
        )
        _, code = self.journal_requester.journal(request, j_uuid)

        return code == 200

    # def add_journal_to_publisher(self, request: Request, p_uuid: str, j_uuid: str) -> Tuple[Dict, int]:
    #     self.loginfo(
    #         msg = '{task_name} {msg}'.format(
    #             task_name = 'ADD_JOURNAL_TO_PUBISHER',
    #             msg = f'adding j_uuid = {j_uuid} to p_uuid = {p_uuid}'
    #         )
    #     )

    #     publisher_json, code = self.get_publisher(request, data)
    #     j_uuid = data['journal']

    #     if filter(lambda x : x['uuid'] == j_uuid):
    #         # j_uuid нет в списке, значит надо добавить его к "издателю"
    #         publisher_json['journals'].append(
    #             {'uuid' : data['publisher']}
    #         )

    #         return self.publisher_requester.patch_publisher(request, publisher_json)

    #     else:
    #         return (publisher_json, code)

    def check_article(self, request: Request, data: dict) -> bool:
        self.loginfo(
            msg = '{task_name} {msg}'.format(
                task_name = 'ARTICLE_CHECK',
                msg = 'checking article'
            )
        )

        try:
            j_uuid = data['journal']

        except KeyError as error:
            raise ArticleError(error)

        return self.journals_exists(request, j_uuid)
