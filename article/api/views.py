from .models import Article, Author
from .serializers import ArticleSerializer

from rest_framework import status, generics
from rest_framework.views import Request, Response, APIView
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination

from django.core.exceptions import FieldError
from django.conf import settings

from uuid import UUID
import logging


DEFAULT_PAGE_LIMIT = settings.DEFAULT_PAGE_LIMIT


class BaseView(APIView):
    logger = logging.getLogger(name = 'article.api.views')
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

class ArticlesView(BaseView):
    def __clear_request_params(self, request: Request) -> dict:
        params = request.query_params.dict()

        if 'limit' in params: params.pop('limit')
        if 'offset' in params: params.pop('offset')

        return params

    def post(self, request: Request) -> Response:
        self.info(request)
        serializer = ArticleSerializer(data = request.data)

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

        author = ''
        if 'author' in params:
            author = params.pop('author')

        article_s = Article.objects.all()

        if author:
            try:
                author_id = Author.objects.get(author_uuid = author)

            except Author.DoesNotExist:
                return Response(data = {'errors' : 'author not found'}, status = status.HTTP_404_NOT_FOUND)


            article_s = article_s.filter(authors__in = [author_id.id])

        try:
            article_s = article_s.filter(**params)
        
        except FieldError as error:
            self.exception(request, f'{error}')
            return Response(
                data = {'errors' : str(error)},
                status = status.HTTP_400_BAD_REQUEST
            )

        paginator = LimitOffsetPagination()
        paginator.default_limit = DEFAULT_PAGE_LIMIT
        paged_article_s = paginator.paginate_queryset(article_s, request)

        serializer = ArticleSerializer(paged_article_s, many = True)

        return Response(
            data = serializer.data,
        )

class ArticleView(BaseView):
    def get(self, request: Request, art_uuid: UUID) -> Response:
        self.info(request)
        try:
            article_ = Article.objects.get(pk = art_uuid)

        except Article.DoesNotExist as error:
            self.exception(request, 'requested art_uuid  not found')
            return Response(
                status = status.HTTP_404_NOT_FOUND
            )

        serializer = ArticleSerializer(instance = article_)

        return Response(data = serializer.data, status = status.HTTP_200_OK)

    def patch(self, request: Request, art_uuid: UUID) -> Response:
        self.info(request)
        try:
            article_ = Article.objects.get(pk = art_uuid)

        except Article.DoesNotExist as error:
            self.exception(request, 'requested art_uuid  not found')
            return Response(status = status.HTTP_404_NOT_FOUND)

        serializer = ArticleSerializer(instance = article_, data = request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(data = serializer.data, status = status.HTTP_202_ACCEPTED)

        self.exception(request, f'not valid data for serializer : {serializer.errors}')
        return Response(data = serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, art_uuid: UUID) -> Response:
        self.info(request)
        try:
            article_ = Article.objects.get(pk = art_uuid)

        except Article.DoesNotExist as error:
            self.exception(request, 'requested art_uuid  not found')
            return Response(status = status.HTTP_404_NOT_FOUND)

        article_.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)