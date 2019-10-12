from rest_framework import status, generics
from rest_framework.views import APIView, Request, Response
from rest_framework.exceptions import ValidationError

import logging

from uuid import UUID

from .serializers import PublisherSerializer
from .models import Publisher

from django.core.exceptions import FieldError

class BaseView(APIView):
    logger = logging.getLogger(name = 'publisher.api.views')

class PublishersView(BaseView):
    def post(self, request: Request) -> Response:
        serializer = PublisherSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                data = serializer.data,
                status = status.HTTP_201_CREATED
            )

        return Response(
            data = serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )

    def get(self, request: Request) -> Response:
        try:
            publisher_s = Publisher.objects.filter(**request.query_params.dict())
        
        except FieldError as error:
            return Response(
                data = {'errors' : str(error)},
                status = status.HTTP_400_BAD_REQUEST
            )

        serializer = PublisherSerializer(publisher_s, many = True)

        return Response(
            data = serializer.data,
        )

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

