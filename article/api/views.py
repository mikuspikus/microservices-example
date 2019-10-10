from .models import Article, Author
from .serializers import ArticleSerializer

from rest_framework import status, generics
from rest_framework.views import Request, Response, APIView

from uuid import UUID

class ArticlesView(generics.ListCreateAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self) -> Response:
        try:
            ath_uuid = self.request.query_params['ath_uuid']

        except KeyError:
            return Response(
                data = { 'error' : '\'ath_uuid\' field not found' },
                status = status.HTTP_400_BAD_REQUEST
            )

        try:
            author_ = Author.object.get(author_uuid = uuid.UUID(ath_uuid))[0]

        except Author.DoesNotExist:
            return Response(
                data = { 'error' : f'No apropriate author for \'ath_uuid\' = {ath_uuid}' },
                status = status.HTTP_404_NOT_FOUND
            )

        articles_ = Article.object.filter(authors = author_)

        return articles_


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