from rest_framework.views import APIView, Request, Response
from rest_framework.renderers import TemplateHTMLRenderer

from django.shortcuts import redirect

from uuid import UUID

from api.requesters.UserRequester import UserRequester
from api.permissions import IsAuthenticatedByAuthenticateService
from api.models import GatewayUser

from .BaseView import BaseView
from api.models import GatewayUser

class BaseUserView(BaseView):
    SERVICE_ERROR_MSG = '\'user\'-service is unavailable'
    requester = UserRequester()

class AuthenticateView(BaseUserView):
    def post(self, request: Request) -> Response:
        self.info(request)

        try:
            response_json, code = self.requester.authenticate(data = request.data)

        except CircuitBreakerError:
            self.exception(self.SERVICE_ERROR_MSG)
            response_json, code = ({'error': self.SERVICE_ERROR_MSG}, status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(response_json, status = code)

class RegisterView(BaseUserView):
    def post(self, request: Request) -> Response:
        self.info(request)

        try:
            response_json, code = self.requester.register(data = request.data)

        except CircuitBreakerError:
            self.exception(self.SERVICE_ERROR_MSG)
            response_json, code = ({'error': self.SERVICE_ERROR_MSG}, status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(response_json, status = code)

class UserInfoView(BaseUserView):
    permission_classes = (IsAuthenticatedByAuthenticateService, )

    def get(self, request: Request) -> Response:
        self.info(request)

        try:
            response_json, code = self.requester.info(request = request)

        except CircuitBreakerError:
            self.exception(self.SERVICE_ERROR_MSG)
            response_json, code = ({'error': self.SERVICE_ERROR_MSG}, status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(response_json, status = code)

    def delete(self, request: Request) -> Response:
        self.info(request)

        try:
            response_json, code = self.requester.delete(request)

        except CircuitBreakerError:
            self.exception(self.SERVICE_ERROR_MSG)
            response_json, code = ({'error': self.SERVICE_ERROR_MSG}, status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(response_json, status = code)

class UsersView(BaseUserView):

    def get(self, request: Request) -> Response:
        self.info(request)

        try:
            response_json, code = self.requester.users(request = request)

        except CircuitBreakerError:
            self.exception(self.SERVICE_ERROR_MSG)
            response_json, code = ({'error': self.SERVICE_ERROR_MSG}, status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(response_json, status = code)

class UserView(BaseUserView):
    permission_classes = (IsAuthenticatedByAuthenticateService, )

    def get(self, request: Request, user_id: int) -> Response:
        self.info(request)

        try:
            response_json, code = self.requester.user(request = request, id_ = user_id)

        except CircuitBreakerError:
            self.exception(self.SERVICE_ERROR_MSG)
            response_json, code = ({'error': self.SERVICE_ERROR_MSG}, status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(response_json, status = code)