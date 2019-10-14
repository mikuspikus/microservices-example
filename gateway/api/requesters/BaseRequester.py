import requests
import json
import logging
import re

from typing import Union, Tuple, List, Any, Dict

from django.conf import settings

DEBUG = settings.DEBUG

from rest_framework.views import Request, Response

class BaseRequester():
    logger = logging.getLogger(name = 'requester')

    URLS = {
        'USER' : 'http://localhost:8081/user/' if DEBUG else '',
        'ARTICLE' : 'http://localhost:8082/articles/' if DEBUG else '',
        'JOURNAL' : 'http://localhost:8083/journals/' if DEBUG else '',
        'PUBLISHER' : 'http://localhost:8084/publishers/' if DEBUG else '',
    }

    TOKENS = {}

    def info(self, request: Request, msg: str = None) -> None:
        self.logger.info(
            self.formatter.format(
                method=request.method,
                url=request._request.get_raw_uri(),
                content_type=request.content_type,
                msg=msg
            )
        )

    def exception(self, request: Request, msg: str = None) -> None:
        self.logger.exception(
            self.formatter.format(
                method=request.method,
                url=request._request.get_raw_uri(),
                content_type=request.content_type,
                msg=msg
            )
        )

    def get(self, url: str, headers: dict = {}) -> Union[requests.Response, None]:
        try:
            self.info(
                '{request_type} {url} {headers}'.format(
                    request_type = 'PUT', 
                    url = url, 
                    headers = headers
                )
            )
            response = requests.get(url = url, headers = headers)

        except requests.exceptions.RequestException as error:
            self.logger.exception(
                '{request_type} {url} {headers} {message}'.format(
                    request_type = 'PUT', 
                    url = url, 
                    headers =headers, 
                    message = str(error)
                )
            )
            return None

        return response

    def post(self, url: str, data: dict = {}, headers: dict = {}) -> Union[requests.Response, None]:
        try:
            self.info(
                '{request_type} {url} {headers}'.format(
                    request_type = 'PUT', 
                    url = url, 
                    headers = headers
                )
            )
            response = requests.post(url = url, json = data, headers = headers)

        except requests.exceptions.RequestException as error:
            self.logger.exception(
                '{request_type} {url} {headers} {message}'.format(
                    request_type = 'PUT', 
                    url = url, 
                    headers =headers, 
                    message = str(error)
                )
            )
            return None

        return response

    def delete(self, url: str, headers: dict = {}) -> Union[requests.Response, None]:
        try:
            self.info(
                '{request_type} {url} {headers}'.format(
                    request_type = 'PUT', 
                    url = url, 
                    headers = headers
                )
            )
            response = requests.delete(url = url, headers = headers)

        except requests.exceptions.RequestException as error:
            self.logger.exception(
                '{request_type} {url} {headers} {message}'.format(
                    request_type = 'PUT', 
                    url = url, 
                    headers =headers, 
                    message = str(error)
                )
            )
            return None

        return response

    def patch(self, url: str, data: dict = {}, headers: dict = {}) -> Union[requests.Response, None]:
        try:
            self.info(
                '{request_type} {url} {headers}'.format(
                    request_type = 'PUT', 
                    url = url, 
                    headers = headers
                )
            )
            response = requests.patch(url = url, json = data, headers = headers)

        except requests.exceptions.RequestException as error:
            self.logger.exception(
                '{request_type} {url} {headers} {message}'.format(
                    request_type = 'PUT', 
                    url = url, 
                    headers =headers, 
                    message = str(error)
                )
            )
            return None

        return response

    def put(self, url: str, data: dict = {}, headers: dict = {}) -> Union[requests.Response, None]:
        try:
            self.info(
                '{request_type} {url} {headers}'.format(
                    request_type = 'PUT', 
                    url = url, 
                    headers = headers
                )
            )
            response = requests.put(url = url, json = data, headers = headers)

        except requests.exceptions.RequestException as error:
            self.logger.exception(
                '{request_type} {url} {headers} {message}'.format(
                    request_type = 'PUT', 
                    url = url, 
                    headers =headers, 
                    message = str(error)
                )
            )
            return None

        return response

    def _token_from_request(self, request: Request) -> str:
        '''
        Raises KeyError
        '''
        token = request.META['HTTP_AUTHORIZATION']
        token = token[7:]

        return token

    def authenticate_header(self, request: Request) -> Union[Dict[str, str], None]:
        try:
            return {'Authorization' : f'Token {self._token_from_request(request)}'}

        except KeyError:
            return None

    def _limit_offset_from_request(self, request: Request) -> Union[Tuple[int, int], None]:
        try:
            limit = request.query_params['limit']
            offset = request.query_params['offset']
        
        except KeyError:
            return None

        return (limit, offset)

    def _limit_offset_from_link(self, link: str) -> Union[Tuple[int, int], None]:
        str_limit, str_offset = re.findall(r'limit=\d+', link), re.findall(r'offset=\d+', link)

        limit = int(re.findall(r'\d+', str_limit[0])) if len(str_limit) else 0
        offset = int(re.findall(r'\d+', str_offset[0])) if len(str_offset) else 0

        return (limit, offset)

    def _next_previous_link(self, data: dict) -> Dict[str, str]:
        try:
            next_link, previous_link = data['next'], data['previous']

        except (KeyError, TypeError):
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

    def _safe_next_previous_link(self, response: Response):
        try:
            return self._next_previous_link(
                data = response.json()
            )

        except ValueError:
            return response.text

    def _process_response(self, response: requests.Response, task_name: str) -> Tuple[Union[Dict[str, str], str], int]:
        '''
        '''
        if response is None:
            self.info(
                f'no valid response from {response.url}'
            )
            return ({'errors' : f'no valid response from {response.url}'}, 504)

        try:
            self.info(
                '{task_name} {code}'.format(
                    task_name = task_name, 
                    code = response.status_code
                )
            )
            return response.json(), response.status_code

        except ValueError as error:
            self.exception(
                '{task_name} {code}'.format(
                    task_name = task_name, 
                    code = response.status_code
                )
            )
            return response.text, response.status_code