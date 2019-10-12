from .models import Article, Author
from .serializers import ArticleSerializer

from rest_framework import status, generics
from rest_framework.views import Request, Response, APIView
from rest_framework.exceptions import ValidationError

from django.core.exceptions import FieldError

from uuid import UUID
import logging

class BaseView(APIView):
    logger = logging.getLogger(name = 'article.api.views')

class ArticlesView(BaseView):
    def post(self, request: Request) -> Response:
        serializer = ArticleSerializer(data = request.data)

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
            article_s = Article.objects.filter(**request.query_params.dict())
        
        except FieldError as error:
            return Response(
                data = {'errors' : str(error)},
                status = status.HTTP_400_BAD_REQUEST
            )

        serializer = ArticleSerializer(article_s, many = True)

        return Response(
            data = serializer.data,
        )

class ArticleView(APIView):
    def get(self, request: Request, art_uuid: UUID) -> Response:
        try:
            article_ = Article.objects.get(pk = art_uuid)

        except Article.DoesNotExist:
            return Response(
                status = status.HTTP_404_NOT_FOUND
            )

        serializer = ArticleSerializer(instance = article_)

        return Response(data = serializer.data, status = status.HTTP_200_OK)

    def patch(self, request: Request, art_uuid: UUID) -> Response:
        try:
            article_ = Article.objects.get(pk = art_uuid)

        except Article.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        serializer = ArticleSerializer(instance = article_, data = request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(data = serializer.data, status = status.HTTP_202_ACCEPTED)

        return Response(data = serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, art_uuid: UUID) -> Response:
        try:
            article_ = Article.objects.get(pk = art_uuid)

        except Article.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        article_.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)