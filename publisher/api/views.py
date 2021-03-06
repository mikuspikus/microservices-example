from rest_framework import status, generics
from rest_framework.views import APIView, Request, Response
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

import logging

from uuid import UUID

from .serializers import PublisherSerializer, AppAuthSerializer
from .models import Publisher, CustomToken

from django.core.exceptions import FieldError
from django.conf import settings

from .authentication import ExpiringTokenAuthentication
from .permissions import IsAuthenticatedByToken


DEFAULT_PAGE_LIMIT = settings.DEFAULT_PAGE_LIMIT

class BaseView(APIView):
    logger = logging.getLogger(name = 'views')
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

class CustomObtainTokenView(BaseView, ObtainAuthToken):
    serializer_class = AppAuthSerializer
    def post(self, request: Request) -> Response:
        self.info(request)
        
        serializer = self.serializer_class(data = request.data, context = {'request': request})
        serializer.is_valid(raise_exception = True)
        token = CustomToken.objects.create()

        return Response(data = {'token': token.token}, status = status.HTTP_200_OK)

class PublishersView(BaseView):
    authentication_classes = (ExpiringTokenAuthentication, )
    permission_classes = (IsAuthenticatedByToken, )

    def __clear_request_params(self, request: Request) -> dict:
        params = request.query_params.dict()

        if 'limit' in params: params.pop('limit')
        if 'offset' in params: params.pop('offset')

        return params

    def post(self, request: Request) -> Response:
        self.info(request)

        serializer = PublisherSerializer(data = request.data)

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

        params = self.__clear_request_params(request)
        
        try:
            publisher_s = Publisher.objects.filter(**params)
        
        except FieldError as error:
            self.exception(request, f'{error}')
            return Response(
                data = {'errors' : str(error)},
                status = status.HTTP_400_BAD_REQUEST
            )

        paginator = LimitOffsetPagination()
        paginator.default_limit = DEFAULT_PAGE_LIMIT
        paged_publisher_s = paginator.paginate_queryset(publisher_s, request)

        serializer = PublisherSerializer(paged_publisher_s, many = True)

        return Response(
            data = serializer.data,
        )

class PublisherView(BaseView):
    authentication_classes = (ExpiringTokenAuthentication, )
    permission_classes = (IsAuthenticatedByToken, )

    def get(self, request: Request, p_uuid: UUID) -> Response:
        self.info(request, f'p_uuid = {p_uuid}')

        try:
            publisher_ = Publisher.objects.get(pk = p_uuid)

        except Publisher.DoesNotExist:
            self.exception(request, 'requested p_uuid  not found')
            return Response(
                status = status.HTTP_404_NOT_FOUND
            )

        serializer = PublisherSerializer(instance = publisher_)

        return Response(data = serializer.data, status = status.HTTP_200_OK)

    def put(self, request: Request, p_uuid: UUID) -> Response:
        self.info(request, f'p_uuid = {p_uuid}')

        try:
            publisher_ = Publisher.objects.get(pk = p_uuid)

        except Publisher.DoesNotExist:
            self.exception(request, 'requested p_uuid  not found')
            return Response(status = status.HTTP_404_NOT_FOUND)

        serializer = PublisherSerializer(instance = publisher_, data = request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(data = serializer.data, status = status.HTTP_202_ACCEPTED)

        self.exception(request, f'not valid data for serializer : {serializer.erros}')
        return Response(data = serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def patch(self, request: Request, p_uuid: UUID) -> Response:
        self.info(request, f'p_uuid = {p_uuid}')

        try:
            publisher_ = Publisher.objects.get(pk = p_uuid)

        except Publisher.DoesNotExist:
            self.exception(request, 'requested p_uuid  not found')
            return Response(status = status.HTTP_404_NOT_FOUND)

        serializer = PublisherSerializer(instance = publisher_, data = request.data, partial = True)

        if serializer.is_valid():
            serializer.save()

            return Response(data = serializer.data, status = status.HTTP_202_ACCEPTED)

        self.exception(request, f'not valid data for serializer : {serializer.erros}')
        return Response(data = serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, p_uuid: UUID) -> Response:
        self.info(request, f'p_uuid = {p_uuid}')

        try:
            publisher_ = Publisher.objects.get(pk = p_uuid)

        except Publisher.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        publisher_.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)

