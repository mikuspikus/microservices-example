from rest_framework.views import APIView, Request, Response
from rest_framework.renderers import TemplateHTMLRenderer
from  rest_framework import status

import logging
from uuid import UUID
from circuitbreaker import CircuitBreakerError

from api.requesters.ArticleRequester import ArticleRequester
from api.permissions import IsAuthenticatedByAuthenticateService

from .BaseView import BaseView

class BaseArticleView(BaseView):
    SERVICE_ERROR_MSG = '\'articles\'-service is unavailable'
    requester = ArticleRequester()

class ArticlesView(BaseArticleView):
    #permission_classes = (IsAuthenticatedByAuthenticateService, )

    def get(self, request: Request) -> Response:
        self.info(request)

        try:
            response_json, code = self.requester.articles(request = request)

        except CircuitBreakerError:
            self.exception(self.SERVICE_ERROR_MSG)
            response_json, code = ({'error': self.SERVICE_ERROR_MSG}, status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(response_json, status = code)

    def post(self, request: Request) -> Response:
        self.info(request)

        try:
            response_json, code = self.requester.post_article(request = request, data = request.data)
        
        except CircuitBreakerError:
            self.exception(self.SERVICE_ERROR_MSG)
            response_json, code = ({'error': self.SERVICE_ERROR_MSG}, status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(response_json, status = code)

class ArticleView(BaseArticleView):
    permission_classes = (IsAuthenticatedByAuthenticateService, )

    def get(self, request: Request, art_uuid: UUID):
        self.info(request)

        try:
            response_json, code = self.requester.article(request = request, uuid = str(art_uuid))

        except CircuitBreakerError:
            self.exception(self.SERVICE_ERROR_MSG)
            response_json, code = ({'error': self.SERVICE_ERROR_MSG}, status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(response_json, status = code)
    
    def patch(self, request: Request, art_uuid: UUID):
        self.info(request)

        try:
            response_json, code = self.requester.patch_article(request = request, data = request.data, uuid = str(art_uuid))

        except CircuitBreakerError:
            self.exception(self.SERVICE_ERROR_MSG)
            response_json, code = ({'error': self.SERVICE_ERROR_MSG}, status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(response_json, status = code)

    def delete(self, request: Request, art_uuid: UUID):
        self.info(request)

        try:
            response_json, code = self.requester.delete_article(request = request, uuid = str(art_uuid))

        except:
            self.exception(self.SERVICE_ERROR_MSG)
            response_json, code = ({'error': self.SERVICE_ERROR_MSG}, status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(response_json, status = code)