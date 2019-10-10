from rest_framework import status, generics
from rest_framework.views import APIView, Request, Response

from logging import Logger

from uuid import UUID

from .serializers import PublisherSerializer
from .models import Publisher, Journal

class BaseView(APIView):
    logger = Logger(name = 'publisher-views-logger')


class ArticlesView(generics.ListCreateAPIView):
    serializer_class = PublisherSerializer

    def get_queryset(self) -> Response:
        try:
            j_uuid = self.request.query_params['j_uuid']

        except KeyError:
            return Response(
                data = { 'error' : '\'j_uuid\' field not found' },
                status = status.HTTP_400_BAD_REQUEST
            )

        try:
            journal_ = Journal.object.get(uuid = uuid.UUID(j_uuid))[0]

        except Journal.DoesNotExist:
            return Response(
                data = { 'error' : f'No apropriate journal for \'j_uuid\' = {j_uuid}' },
                status = status.HTTP_404_NOT_FOUND
            )

        publisher_ = Publisher.object.filter(journals = author_)

        return publisher_


class PublisherView(APIView):
    def get(self, request: Request, p_uuid: UUID) -> Response:
        try:
            publisher_ = Publisher.objects.get(pk = p_uuid)

        except Publisher.DoesNotExist:
            return Response(
                status = status.HTTP_404_NOT_FOUND
            )

        serializer = PublisherSerializer(instance = publisher_)

        return Response(data = serializer.data, status = status.HTTP_200_OK)

    def patch(self, request: Request, p_uuid: UUID) -> Response:
        try:
            publisher_ = Publisher.objects.get(pk = p_uuid)

        except Publisher.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        serializer = PublisherSerializer(instance = publisher_, data = request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(data = serializer.data, status = status.HTTP_202_ACCEPTED)

        return Response(data = serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, p_uuid: UUID) -> Response:
        try:
            publisher_ = Publisher.objects.get(pk = p_uuid)

        except Publisher.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        publisher_.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)

