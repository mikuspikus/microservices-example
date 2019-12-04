from circuitbreaker import CircuitBreakerError
import json
from logging import Logger
from typing import Union, Tuple, List, Any, Dict

from gateway.settings import DEBUG
from .BaseRequester import BaseRequester, CustomCurcuitBreaker
from .PublisherRequester import PublisherRequester

from rest_framework.views import Request, status

class PublisherError(Exception):
    pass

JournalCB = CustomCurcuitBreaker()

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

    @JournalCB
    def journals(self, request: Request) -> Tuple[Dict[str, str], int]:
        url = self.URL

        '''
        u_json, code = self.__user_by_token(request)
        
        if code != 200:
            return (u_json, code)

        url += f'?user_id={u_json["id"]}'
        '''

        limitoffset = self._limit_offset_from_request(request)

        if limitoffset:
            url += f'&limit={limitoffset[0]}&offset={limitoffset[1]}'

        try:
            response = self.get(
                url = url,
            )

        except CircuitBreakerError:
            self.logexception(self.SERVICE_ERROR_MSG)
            return ({'error': self.SERVICE_ERROR_MSG}, status.HTTP_503_SERVICE_UNAVAILABLE)

        response_json, code = self._process_response(
            response = response,
            task_name = 'JOURNALS'
        )

        response_json = self._safe_next_previous_link(
            response = response
        )

        return (response_json, response.status_code)

    @JournalCB
    def journal(self, request: Request, uuid: str) -> Tuple[Dict[str, str], int]:
        try:
            response = self.get(
                url = self.URL + f'{uuid}/'
            )

        except CircuitBreakerError:
            self.logexception(self.SERVICE_ERROR_MSG)
            return ({'error': self.SERVICE_ERROR_MSG}, status.HTTP_503_SERVICE_UNAVAILABLE)


        return self._process_response(
            response = response,
            task_name = 'JOURNAL'
        )

    @JournalCB
    def post_journal(self, request: Request, data: dict) -> Tuple[Dict[str, str], int]:
        # try:
        #     is_journal_valid = self.check_journal(request, data)

        # except PublisherError as error:
        #     return ({'error' : str(error)}, status.HTTP_400_BAD_REQUEST)

        # if not is_journal_valid:
        #     return ({'error' : 'publisher not found'}, status.HTTP_404_NOT_FOUND)

        response = self.post(
            url = self.URL,
            data = data
        )

        return self._process_response(
            response = response,
            task_name = 'POST_JOURNAL'
        )

    @JournalCB
    def patch_journal(self, request: Request, data: dict, uuid: str) -> Tuple[Dict[str, str], int]:
        try:
            is_journal_valid = self.check_journal(request, data)

        except PublisherError as error:
            return ({'errors' : str(error)}, status.HTTP_400_BAD_REQUEST)

        if not is_journal_valid:
            return ({'errors' : 'publisher not found'}, status.HTTP_404_NOT_FOUND)

        response = self.patch(
            url = self.URL + f'{uuid}/',
            data = data
        )

        return self._process_response(
            response = response,
            task_name = 'PATCH_ARTICLE'
        )

    @JournalCB
    def delete_journal(self, request: Request, data: dict, uuid: str) -> Tuple[Dict[str, str], int]:
        journal_json, code = self.journal(request, uuid)

        if code != 200:
            return journal_json, code

        response = self.delete(
            url = self.URL + f'{uuid}/'
        )

        return self._process_response(
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
            p_uuid = data['publisher']

        except KeyError as error:
            raise PublisherError(error)

        return self.publisher_exists(request, p_uuid)