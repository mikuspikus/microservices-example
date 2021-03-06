from rest_framework.views import APIView, Request, Response, status
from rest_framework.renderers import TemplateHTMLRenderer

from django.shortcuts import redirect
from django.conf import settings

from uuid import UUID

from api.requesters.PublisherRequester import PublisherRequester
from api.permissions import IsAuthenticatedByAuthenticateService

from circuitbreaker import CircuitBreakerError
from requests.exceptions import RequestException

from .BaseView import BaseView

class BasePublisherView(BaseView):
    APP_ID = settings.PUBLISHER_CREDENTIALS['id']
    APP_SECRET = settings.PUBLISHER_CREDENTIALS['secret']

    SERVICE_ERROR_MSG = '\'publisher\'-service is unavailable'
    requester = PublisherRequester()

class PublishersView(BasePublisherView):
    permission_classes = (IsAuthenticatedByAuthenticateService, )

    def get(self, request: Request) -> Response:
        self.info(request)
        try:
            response_json, code = self.requester.publishers(request = request)

        except (CircuitBreakerError, RequestException) as error:
            self.exception(request, error)
            response_json, code = ({'error': self.SERVICE_ERROR_MSG}, status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(response_json, status = code)

    def post(self, request: Request) -> Response:
        self.info(request)

        try:
            response_json, code = self.requester.post_publisher(request = request, data = request.data)

        except (CircuitBreakerError, RequestException) as error:
            self.exception(request, error)
            response_json, code = ({'error': self.SERVICE_ERROR_MSG}, status.HTTP_503_SERVICE_UNAVAILABLE)

        return redirect('publishers')

class PublisherView(BasePublisherView):
    permission_classes = (IsAuthenticatedByAuthenticateService, )

    def get(self, request: Request, p_uuid: UUID):
        self.info(request)

        try:
            response_json, code = self.requester.publisher(request = request, uuid = str(p_uuid))

        except (CircuitBreakerError, RequestException) as error:
            self.exception(request, error)
            response_json, code = ({'error': self.SERVICE_ERROR_MSG}, status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(response_json, status = code)

    def patch(self, request: Request, p_uuid: UUID):
        self.info(request)

        try:
            response_json, code = self.requester.patch_publisher(request = request, data = request.data, uuid = str(p_uuid))

        except (CircuitBreakerError, RequestException) as error:
            self.exception(request, error)
            response_json, code = ({'error': self.SERVICE_ERROR_MSG}, status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(response_json, status = code)

    def delete(self, request: Request, p_uuid: UUID):
        self.info(request)

        try:
            response_json, code = self.requester.delete_publisher(request = request, uuid = str(p_uuid))

        except (CircuitBreakerError, RequestException) as error:
            self.exception(request, error)
            response_json, code = ({'error': self.SERVICE_ERROR_MSG}, status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(response_json, status = code)