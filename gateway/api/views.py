from django.shortcuts import render

from rest_framework.views import APIView, Request, Response

from logging import Logger

from api.requesters import UserRequester
from api.permissions import IsAuthenticatedByAuthenticateService

class BaseUserView(APIView):
    requester = UserRequester()
    logger = Logger(name = 'gateway-user-views-logger')

class AuthenticateView(BaseUserView):
    def post(self, request: Request) -> Response:
        response_json, code = self.requester.authenticate(data = request.data)

        return Response(response_json, status = code)

class RegisterView(BaseUserView):
    def post(self, request: Request) -> Response:
        response_json, code = self.requester.register(data = request.data)

        return Response(response_json, status = code)

class UserInfoView(BaseUserView):
    permission_classes = (IsAuthenticatedByAuthenticateService, )

    def get(self, request: Request) -> Response:
        response_json, code = self.requester.info(request = request)

        return Response(response_json, status = code)

    def delete(self, request: Request) -> Response:
        response_json, code = self.requester.delete(request)

        return Response(response_json, status = code)

class UsersView(BaseUserView):
    permission_classes = (IsAuthenticatedByAuthenticateService, )

    def get(self, request: Request) -> Response:
        response_json, code = self.requester.users(request = request)

        return Response(response_json, status = code)

class UserView(BaseUserView):
    permission_classes = (IsAuthenticatedByAuthenticateService, )

    def get(self, request: Request, user_id: int) -> Response:
        response_json, code = self.requester.user(request = request, id_ = user_id)

        return Response(response_json, status = code)
