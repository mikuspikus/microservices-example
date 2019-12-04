from rest_framework.views import Request, status
from typing import Union, Tuple, List, Any, Dict
from circuitbreaker import CircuitBreakerError
from requests.exceptions import RequestException

from .BaseRequester import BaseRequester, CustomCurcuitBreaker

from .ArticleRequester import ArticleRequester
from .JournalRequester import JournalRequester
from .PublisherRequester import PublisherRequester
from .UserRequester import UserRequester

# from fpqueue.PublisherQueueJob import PublsiherQueueJob
# from rq import Queue, use_connection

import cqueue.tasks as tasks

ComplexCB = CustomCurcuitBreaker()
# use_connection()

class ComplexRequester(BaseRequester):

    article_req = ArticleRequester()
    journal_req = JournalRequester()
    publisher_req = PublisherRequester()
    user_req = UserRequester()

    # pqueue = Queue('publisher')

    __ARTICLESERVICE_UNAVAILABLE_ERR = '\'article\' service is unavailable'
    __JOURNALSERVICE_UNAVAILABLE_ERR = '\'journal\' service is unavailable'
    __PUBLISHERSERVICE_UNAVAILABLE_ERR = '\'publisher\' service is unavailable'
    __USERSERVICE_UNAVAILABLE_ERR = '\'user\' service is unavailable'
    
    __BAD_USER_ERROR = 'bad user data'
    __BAD_ARTICLE_ERROR = 'bad article data'
    __BAD_JOURNAL_ERROR = 'bad journal data'
    __BAD_PUBLISHER_ERROR = 'bad publisher data'

    __PUBLISHER_ENQUEUED = 'task enqueued'

    def journal_and_publisher(self, request: Request, data: dict) -> Tuple[Dict[str, str], int]:
        try:
            journal_s_data = data['journals']

        except KeyError:
            self.logexception(self.__BAD_JOURNAL_ERROR)
            return ({'error': self.__BAD_JOURNAL_ERROR}, status.HTTP_400_BAD_REQUEST)

        j_uuid_s =[]

        try:
            publisher_data = data['publisher']

        except KeyError:
            self.logexception(self.__BAD_PUBLISHER_ERROR)
            return ({'error': self.__BAD_PUBLISHER_ERROR}, status.HTTP_400_BAD_REQUEST)

        for journal_data in journal_s_data:
            try:
                j_json, code = self.journal_req.post_journal(request, journal_data)

                if code != 201:
                    return (j_json, code)

                j_uuid_s.append({'uuid': j_json['uuid']})

            except (CircuitBreakerError, RequestException) as error:
                self.logexception(error)
                return ({'error': self.__BAD_JOURNAL_ERROR}, status.HTTP_503_SERVICE_UNAVAILABLE)

        try:
            publisher_data['journals'] = j_uuid_s
            p_json, code = self.publisher_req.post_publisher(request, publisher_data)

        except (CircuitBreakerError, RequestException) as error:
            self.loginfo(error)
            tasks.post.delay({'data': publisher_data, 'headers': {}})
            return ({'error': self.__PUBLISHER_ENQUEUED}, status.HTTP_201_CREATED)

        return (p_json, code)


    def journal_and_article(self, request: Request, data: dict) -> Tuple[Dict[str, str], int]:
        try:
            article_data = data['article']

        except KeyError:
            self.logexception(self.__BAD_ARTICLE_ERROR)
            return ({'error': self.__BAD_ARTICLE_ERROR}, status.HTTP_400_BAD_REQUEST)

        try:
            journal_data = data['journal']

        except KeyError:
            self.logexception(request, self.__BAD_JOURNAL_ERROR)
            return ({'error': self.__BAD_JOURNAL_ERROR}, status.HTTP_400_BAD_REQUEST)

        try:
            j_json, code = self.journal_req.post_journal(request, journal_data)

        except (CircuitBreakerError, RequestException):
            self.logexception(self.__JOURNALSERVICE_UNAVAILABLE_ERR)
            return ({'error': self.__JOURNALSERVICE_UNAVAILABLE_ERR}, status.HTTP_503_SERVICE_UNAVAILABLE)

        if code != 201:
            return (j_json, code)

        article_data['journal'] = j_json['uuid']

        try:
            a_json, code = self.article_req.post_article(request, article_data)

        except (CircuitBreakerError, RequestException):
            self.logexception(self.__ARTICLESERVICE_UNAVAILABLE_ERR)
            j_json, code = self.journal_req.delete_journal(request, {}, j_json['uuid'])
            return ({'error': self.__ARTICLESERVICE_UNAVAILABLE_ERR}, status.HTTP_503_SERVICE_UNAVAILABLE)

        if code == 200:
            return (a_json, code)

        self.journal_req.delete_journal(request, {}, j_json['uuid'])

        return ({'error': self.__BAD_ARTICLE_ERROR}, status.HTTP_400_BAD_REQUEST)

    def user_articles(self, request: Request, user_id: int) -> Tuple[Dict[str, str], int]:
        try:
            u_json, code = self.user_req.user(request = request, id_ = user_id)

        except (CircuitBreakerError, RequestException):
            self.logexception(self.__USERSERVICE_UNAVAILABLE_ERR)
            return ({'error': self.__USERSERVICE_UNAVAILABLE_ERR}, status.HTTP_503_SERVICE_UNAVAILABLE)

        if code != 200:
            return ({'error' : self.__BAD_USER_ERROR}, status.HTTP_404_NOT_FOUND)

        u_uuid = u_json['outer_uuid']

        try:
            arts_json, code = self.article_req.user_articles(request, author = u_uuid)

        except (CircuitBreakerError, RequestException):
            return ({'error': self.__ARTICLESERVICE_UNAVAILABLE_ERR}, status.HTTP_503_SERVICE_UNAVAILABLE)

        if code != 200:
            return (arts_json, code)

        result = []

        for article in arts_json:
            j_uuid = article['journal']

            try:
                journal_json, code = self.journal_req.journal(request, j_uuid)

            except (CircuitBreakerError, RequestException):
                self.logexception(self.__JOURNALSERVICE_UNAVAILABLE_ERR)
                return (arts_json, code)

            if code != 200:
                journal_json = {'error' : {f'journal with uuid = \'{j_uuid}\' not found'}}

            journal_json.pop('uuid')

            result.append(
                {
                    **article,
                    **{
                        f'j_{key}': journal_json[key] for key in journal_json
                    }
                }
            )

        return (result, code)

    def user_journals(self, request: Request, user_id: int) -> Tuple[Dict[str, str], int]:
        try:
            u_json, code = self.user_req.user(request, id_ = user_id)

        except (CircuitBreakerError, RequestException):
            self.logexception(self.__USERSERVICE_UNAVAILABLE_ERR)
            return ({'error': self.__USERSERVICE_UNAVAILABLE_ERR}, status.HTTP_503_SERVICE_UNAVAILABLE)

        if code != 200:
            return ({'error' : self.__BAD_USER_ERROR}, status.HTTP_404_NOT_FOUND)

        u_uuid = u_json['outer_uuid']

        try:
            arts_json, code = self.article_req.user_articles(request, author = u_uuid)

        except (CircuitBreakerError, RequestException):
            self.logexception(self.__ARTICLESERVICE_UNAVAILABLE_ERR)
            return ({'error': self.__ARTICLESERVICE_UNAVAILABLE_ERR}, status.HTTP_503_SERVICE_UNAVAILABLE)

        if code != 200:
            return ({'error' : __BAD_ARTICLE_ERROR}, status.HTTP_404_NOT_FOUND)

        journals = []

        for art_json in arts_json:
            j_uuid = art_json['journal']

            try:
                journal_json, code = self.journal_req.journal(request, j_uuid)

            except (CircuitBreakerError, RequestException):
                self.logexception(self.__JOURNALSERVICE_UNAVAILABLE_ERR)
                return ({'error': self.__JOURNALSERVICE_UNAVAILABLE_ERR}, status.HTTP_503_SERVICE_UNAVAILABLE)

            if code != 200:
                journal_json = {'error' : {f'journal with uuid = \'{j_uuid}\' not found'}}

            journals.append(journal_json)

        return (journals, status.HTTP_200_OK)