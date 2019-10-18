from rest_framework import status, generics
from rest_framework.views import APIView, Request, Response
from rest_framework.exceptions import ValidationError

import logging

from uuid import UUID

from .serializers import PublisherSerializer
from .models import Publisher

from django.core.exceptions import FieldError

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

class PublishersView(BaseView):
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
        
        try:
            publisher_s = Publisher.objects.filter(**request.query_params.dict())
        
        except FieldError as error:
            self.exception(request, f'{error}')
            return Response(
                data = {'errors' : str(error)},
                status = status.HTTP_400_BAD_REQUEST
            )

        serializer = PublisherSerializer(publisher_s, many = True)

        return Response(
            data = serializer.data,
        )

class PublisherView(BaseView):
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

