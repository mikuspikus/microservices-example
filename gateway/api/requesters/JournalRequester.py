import requests
import json
from logging import Logger
from typing import Union, Tuple, List, Any, Dict

from gateway.settings import DEBUG
from .BaseRequester import BaseRequester
from .PublisherRequester import PublisherRequester

from rest_framework.views import Request

class PublisherError(Exception):
    pass

class JournalRequester(BaseRequester):
    URL = ''

    publisher_requester = PublisherRequester()

    def __init__(self):
        self.URL = self.URLS['JOURNAL']

    def __user_exists(self, request: Request, u_id: int) -> bool:
        from api.requesters.UserRequester import UserRequester

        _, code = UserRequester().user(request = request, id_ = u_id)

        return code == 200

    def __user_by_token(self, request: Request) -> Tuple[Dict[str, str], int]:
        from api.requesters.UserRequester import UserRequester

        u_json, code = UserRequester().info(request = request)

        return u_json, code

    def journals(self, request: Request) -> Tuple[Dict[str, str], int]:
        url = self.URL

        u_json, code = self.__user_by_token(request)

        if code != 200:
            return (u_json, code)

        url += f'?user_id={u_json["id"]}'

        limitoffset = self._limit_offset_from_request(request)

        if limitoffset:
            url += f'&limit={limitoffset[0]}&offset={limitoffset[1]}'

        response = self.get(
            url = url,
        )

        response_json, code = self._process_response(
            response = response,
            task_name = 'JOURNALS'
        )

        response_json = self._safe_next_previous_link(
            response = response
        )

        return (response_json, response.status_code)

    def journal(self, request: Request, uuid: str) -> Tuple[Dict[str, str], int]:
        response = self.get(
            url = self.URL + f'{uuid}/'
        )

        return self._process_response(
            response = response,
            task_name = 'JOURNAL'
        )

    def post_journal(self, request: Request, data: dict) -> Tuple[Dict[str, str], int]:
        try:
            is_journal_valid = self.check_journal(request, data)

        except PublisherError as error:
            return ({'errors' : str(error)}, status.HTTP_400_BAD_REQUEST)

        if not PublisherError:
            return ({'errors' : 'journal not found'}, status.HTTP_404_NOT_FOUND)

        response = self.post(
            url = self.URL,
            data = data
        )

        return response._process_response(
            response = response,
            task_name = 'POST_JOURNAL'
        )

    def patch_journal(self, request: Request, data: dict, uuid: str) -> Tuple[Dict[str, str], int]:
        try:
            is_journal_valid = self.check_journal(request, data)

        except PublisherError as error:
            return ({'errors' : str(error)}, status.HTTP_400_BAD_REQUEST)

        if not PublisherError:
            return ({'errors' : 'journal not found'}, status.HTTP_404_NOT_FOUND)

        response = self.patch(
            url = self.URL + f'{uuid}/',
            data = data
        )

        return response._process_response(
            response = response,
            task_name = 'PATCH_ARTICLE'
        )

    def delete_journal(self, request: Request, data: dict, uuid: str) -> Tuple[Dict[str, str], int]:
        journal_json, code = self.journal(request, uuid)

        if code != 200:
            return journal_json, code

        response = self.delete(
            url = self.URL + f'{uuid}/',
            data = data
        )

        return response._process_response(
            response = response,
            task_name = 'DELETE_JOURNAL'
        )

    def get_publisher(self, request: Request, p_uuid: str) -> Tuple[Dict, int]:
        self.loginfo(
            '{task_name} {msg}'.format(
                task_name = 'PUBLISHER_GET',
                msg = f'getting with p_uuid = {p_uuid}'
            )
        )
        p_json, code = self.publisher_requester.publisher(request, p_uuid)

        return (p_json, code)

    def publisher_exists(self, request: Request, p_uuid: str) -> bool:
        self.loginfo(
            '{task_name} {msg}'.format(
                task_name = 'PUBLISHER_EXISTS',
                msg = f'checking with p_uuid = {p_uuid}'
            )
        )
        _, code = self.get_publisher(request, p_uuid)
        return code == 200

    def check_journal(self, request: Request, data: dict) -> bool:
        self.loginfo(
            msg = '{task_name} {msg}'.format(
                task_name = 'JOURNAL_CHECK',
                msg = 'checking journal'
            )
        )

        try:
            j_uuid = data['publisher']

        except KeyError as error:
            raise PublisherError(error)

        return self.journals_exists(request, j_uuid)