from django.shortcuts import render

from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView, Request, Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from api.serializers import CustomUserSerializer
from api.models import CustomUser

from logging import Logger

class BaseView(APIView):
    logger = Logger(name = 'views')
    formatter = '{method} : {url} : {content_type} : {msg}'

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

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        self.info(request)

        serializer = self.serializer_class(data = request.data, context = {'request': request})
        serializer.is_valid(raise_exception = True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user = user)

        return Response({'token': token.key, 'user_id': user.pk, 'uuid' : user.outer_uuid}, status = status.HTTP_200_OK)

class UserInfoView(BaseView):

    permission_classes = (IsAuthenticated, )

    def get(self, request: Request, *args, **kwargs) -> Response:
        self.info(request, request.user)

        if request.user is None:
            return Response(status = status.HTTP_400_BAD_REQUEST)

        serializer = CustomUserSerializer(instance = request.user)

        return Response(data = serializer.data, status = status.HTTP_200_OK)

    def patch(self, request: Request) -> Response:
        self.info(request, request.user)

        if request.user is None:
            return Response(status = status.HTTP_400_BAD_REQUEST)

        serializer = CustomUserSerializer(instance = request.user, data = request.data)
        
        if serializer.is_valid():
            serializer.save()

            return Response(data = serializer.data, status = status.HTTP_202_ACCEPTED)

        self.exception(request, f'not valid data for serializer : {serializer.errors}')
        return Response(data = serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request) -> Response:
        self.info(request, request.user)

        if request.user is None:
            return Response(status = status.HTTP_400_BAD_REQUEST)

        request.user.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)


class UsersView(BaseView):
    permission_classes = (IsAuthenticated, )

    def post(self, request: Request) -> Response:
        self.info(request)
        serializer = CustomUserSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                data = serializer.data,
                status = status.HTTP_201_CREATED
            )

        self.exception(request, f'not valid data for serializer : {serializer.errors}')
        return Response(
            data = serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )

    def get(self, request: Request) -> Response:
        self.info(request)

        user_s = CustomUser.objects.all()
        serializer = CustomUserSerializer(user_s, many = True)

        return Response(
            data = serializer.data,
        )


class UserView(BaseView):
    permissions_classes = (IsAuthenticated, )

    def get(self, request: Request, user_id: int) -> Response:
        try:
            user_ = CustomUser.objects.get(id = user_id)

        except CustomUser.DoesNotExist:
            self.exception(request, f'user not found')
            return Response(status = status.HTTP_404_NOT_FOUND)

        serializer = CustomUserSerializer(instance = user_)

        return Response(data = serializer.data, status = status.HTTP_200_OK)


class RegisterView(BaseView):
    def post(self, request : Request, *args, **kwargs) -> Response:
        serializer = CustomUserSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(data = serializer.data, status = status.HTTP_201_CREATED)

        self.exception(request, f'not valid data for serializer : {serializer.errors}')
        return Response(data = serializer.errors, status = status.HTTP_400_BAD_REQUEST)