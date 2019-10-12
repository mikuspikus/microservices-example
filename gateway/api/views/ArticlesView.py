from rest_framework.views import APIView, Request, Response

import logging
from uuid import UUID

from api.requesters.ArticleRequester import ArticleRequester
from api.permissions import IsAuthenticatedByAuthenticateService

class BaseArticleView(APIView):
    requester = ArticleRequester()
    logger = logging.getLogger(name = 'gateway.api.views')

class ArticlesView(BaseArticleView):
    permission_classes = (IsAuthenticatedByAuthenticateService, )

    def get(self, request: Request) -> Response:
        response_json, code = self.requester.articles(request = request)

        return Response(response_json, status = code)

    def post(self, request: Request) -> Response:
        response_json, code = self.requester.post_article(request = request, data = request.data)

        return Response(response_json, status = code)

class ArticleView(BaseArticleView):
    permission_classes = (IsAuthenticatedByAuthenticateService, )

    def get(self, request: Request, art_uuid: UUID):
        response_json, code = self.requester.article(request = request, uuid = str(art_uuid))

        return Response(response_json, status = code)
    
    def patch(self, request: Request, art_uuid: UUID):
        response_json, code = self.requester.patch_article(request = request, data = request.data, uuid = str(art_uuid))

        return Response(response_json, status = code)

    def delete(self, request: Request, art_uuid: UUID):
        response_json, code = self.requester.delete_article(request = request, uuid = str(art_uuid))

        return Response(response_json, status = code)