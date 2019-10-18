from rest_framework import status, generics
from rest_framework.views import APIView, Request, Response
from rest_framework.pagination import LimitOffsetPagination

from django.conf import settings
from django.core.exceptions import FieldError

import logging
from sys import stdout

from uuid import UUID

from .serializers import JournalSerializer
from .models import Journal


DEFAULT_PAGE_LIMIT = settings.DEFAULT_PAGE_LIMIT


class BaseView(APIView):
    logger = logging.getLogger(name='views')
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


class JournalsView(BaseView):
    def __clear_request_params(self, request: Request) -> dict:
        params = request.query_params.dict()

        if 'limit' in params: params.pop('limit')
        if 'offset' in params: params.pop('offset')

        return params

    def post(self, request: Request) -> Response:
        self.info(request)
        serializer = JournalSerializer(data = request.data)

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
            journals_s = Journal.objects.filter(**params)
        
        except FieldError as error:
            self.exception(request, f'{error}')
            return Response(
                data = {'errors' : str(error)},
                status = status.HTTP_400_BAD_REQUEST
            )

        paginator = LimitOffsetPagination()
        paginator.default_limit = DEFAULT_PAGE_LIMIT
        paged_journal_s = paginator.paginate_queryset(journals_s, request)

        serializer = JournalSerializer(paged_journal_s, many = True)

        return Response(
            data = serializer.data,
        )


class JournalView(BaseView):
    def get(self, request: Request, j_uuid: UUID) -> Response:
        self.info(request, f'j_uuid = {j_uuid}')

        try:
            journal_ = Journal.objects.get(pk=j_uuid)

        except Journal.DoesNotExist:
            self.exception(request, f'j_uuid = {j_uuid} not found')

            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = JournalSerializer(instance=journal_)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, j_uuid: UUID) -> Response:
        self.info(request, f'j_uuid = {j_uuid}')

        try:
            journal_ = Journal.objects.get(pk=j_uuid)

        except Journal.DoesNotExist:
            self.exception(request, f'j_uuid = {j_uuid} not found')

            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = JournalSerializer(instance=journal_, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, j_uuid: UUID) -> Response:
        self.info(request, f'j_uuid = {j_uuid}')

        try:
            journal_ = Journal.objects.get(pk=j_uuid)

        except Journal.DoesNotExist:
            self.exception(request, f'j_uuid = {j_uuid} not found')

            return Response(status=status.HTTP_404_NOT_FOUND)

        journal_.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
