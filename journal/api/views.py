from rest_framework import status, generics
from rest_framework.views import APIView, Request, Response

import logging
from sys import stdout

from uuid import UUID

from .serializers import JournalSerializer
from .models import Journal


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


class JournalsView(BaseView, generics.ListCreateAPIView):
    serializer_class = JournalSerializer
    queryset = Journal.objects.all()


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
