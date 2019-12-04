from rest_framework.views import APIView, Request, Response, status

import logging
from uuid import UUID
from circuitbreaker import CircuitBreakerError

from api.requesters.ComplexRequester import ComplexRequester
from api.permissions import IsAuthenticatedByAuthenticateService

from .BaseView import BaseView

class BaseComplexView(BaseView):
    complex_requster = ComplexRequester()
    
    _ARTICLESERVICE_ERROR = '\'article\' service responded with error'
    _USERSERVICE_ERROR = '\'user\' service responded with error'
    _JOURNALSERVICE_ERROR = '\'journal\' service responded with error'
    _PUBLISHERSERVICE_ERROR = '\'publisher\' service responded with error'


class UserArticlesView(BaseComplexView):
    permission_classes = (IsAuthenticatedByAuthenticateService, )

    def get(self, request: Request, user_id: int) -> Response:
        self.info(request)
        
        response_json, code = self.complex_requster.user_articles(request = request, user_id = user_id)

        return Response(response_json, status = code)


class UserJournalsView(BaseComplexView):
    permission_classes = (IsAuthenticatedByAuthenticateService, )

    def get(self, request: Request, user_id: int) -> Response:
        self.info(request)

        response_json, code = self.complex_requster.user_journals(request, user_id)

        return Response(data = response_json, status = code)


class ArticleAndJournalView(BaseComplexView):
    def post(self, request: Request) -> Response:
        self.info(request)

        response_json, code = self.complex_requster.journal_and_article(request, request.data)

        return Response(data = response_json, status = code)

class JournalAndPublisherView(BaseComplexView):

    def post(self, request: Request) -> Response:
        self.info(request)

        response_json, code = self.complex_requster.journal_and_publisher(request, request.data)

        return Response(data = response_json, status = code)