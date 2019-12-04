from rest_framework.views import APIView, Request, Response
from rest_framework.renderers import TemplateHTMLRenderer

import logging
from requests.exceptions import RequestException

from uuid import UUID
from requests.exceptions import RequestException
from circuitbreaker import CircuitBreakerError

from api.requesters.JournalRequester import JournalRequester
from api.permissions import IsAuthenticatedByAuthenticateService

from .BaseView import BaseView

class BaseJournalView(BaseView):
    SERVICE_ERROR_MSG = '\'journal\'-service is unavailable'
    requester = JournalRequester()

class JournalsView(BaseJournalView):
    #permission_classes = (IsAuthenticatedByAuthenticateService, )

    def get(self, request: Request) -> Response:
        self.info(request)

        try:
            response_json, code = self.requester.journals(request = request)

        except RequestException:
            self.exception(self.SERVICE_ERROR_MSG)
            response_json, code = ({'error': self.SERVICE_ERROR_MSG}, status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(response_json, status = code)

    def post(self, request: Request) -> Response:
        self.info(request)

        try:
            response_json, code = self.requester.post_journal(request = request, data = request.data)

        except RequestException:
            self.exception(self.SERVICE_ERROR_MSG)
            response_json, code = ({'error': self.SERVICE_ERROR_MSG}, status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(response_json, status = code)

class JournalView(BaseJournalView):
    #permission_classes = (IsAuthenticatedByAuthenticateService, )

    def get(self, request: Request, j_uuid: UUID):
        self.info(request)

        try:
            response_json, code = self.requester.journal(request = request, uuid = str(j_uuid))

        except RequestException:
            self.exception(self.SERVICE_ERROR_MSG)
            response_json, code = ({'error': self.SERVICE_ERROR_MSG}, status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(response_json, status = code)
    
    def patch(self, request: Request, j_uuid: UUID):
        self.info(request)

        try:
            response_json, code = self.requester.patch_journal(request = request, data = request.data, uuid = str(j_uuid))

        except RequestException:
            self.exception(self.SERVICE_ERROR_MSG)
            response_json, code = ({'error': self.SERVICE_ERROR_MSG}, status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(response_json, status = code)

    def delete(self, request: Request, j_uuid: UUID):
        self.info(request)

        try:
            response_json, code = self.requester.delete_journal(request = request, uuid = str(j_uuid))

        except RequestException:
            self.exception(self.SERVICE_ERROR_MSG)
            response_json, code = ({'error': self.SERVICE_ERROR_MSG}, status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(response_json, status = code)