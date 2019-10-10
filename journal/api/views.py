from rest_framework import status, generics
from rest_framework.views import APIView, Request, Response

from logging import Logger

from uuid import UUID

from .serializers import JournalSerializer
from .models import Journal

class BaseView(APIView):
    logger = Logger(name = 'journal-views-logger')


class JournalsView(BaseView, generics.ListCreateAPIView):
    serializer_class = JournalSerializer
    queryset = Journal.objects.all()


class JournalView(BaseView):
    def get(self, request: Request, j_uuid: UUID) -> Response:
        try:
            journal_ = Journal.objects.get(pk = j_uuid)

        except Journal.DoesNotExist:
            return Response(
                status = status.HTTP_404_NOT_FOUND
            )

        serializer = JournalSerializer(instance = journal_)

        return Response(data = serializer.data, status = status.HTTP_200_OK)

    def patch(self, request: Request, j_uuid: UUID) -> Response:
        try:
            journal_ = Journal.objects.get(pk = j_uuid)

        except Journal.DoesNotExist:
            return Response(
                status = status.HTTP_404_NOT_FOUND
            )

        serializer = JournalSerializer(instance = journal_, data = request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(data = serializer.data, status = status.HTTP_202_ACCEPTED)

        return Response(data = serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, j_uuid: UUID) -> Response:
        try:
            journal_ = Journal.objects.get(pk = art_uuid)

        except Journal.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        journal_.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)