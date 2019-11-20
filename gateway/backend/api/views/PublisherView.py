from rest_framework.views import APIView, Request, Response
from rest_framework.renderers import TemplateHTMLRenderer

from django.shortcuts import redirect

from uuid import UUID

from api.requesters.PublisherRequester import PublisherRequester
from api.permissions import IsAuthenticatedByAuthenticateService

from .BaseView import BaseView

class BasePublisherView(BaseView):
    requester = PublisherRequester()

class PublishersView(BasePublisherView):
    #permission_classes = (IsAuthenticatedByAuthenticateService, )

    def get(self, request: Request) -> Response:
        self.info(request)
        response_json, code = self.requester.publishers(request = request)

        return Response(response_json, status = code)

    def post(self, request: Request) -> Response:
        self.info(request)
        response_json, code = self.requester.post_publisher(request = request, data = request.data)

        return redirect('publishers')

class PublisherView(BasePublisherView):
    permission_classes = (IsAuthenticatedByAuthenticateService, )

    def get(self, request: Request, p_uuid: UUID):
        self.info(request)
        response_json, code = self.requester.publisher(request = request, uuid = str(p_uuid))

        return Response(response_json, status = code)
    
    def patch(self, request: Request, p_uuid: UUID):
        self.info(request)
        response_json, code = self.requester.patch_publisher(request = request, data = request.data, uuid = str(p_uuid))

        return Response(response_json, status = code)

    def delete(self, request: Request, p_uuid: UUID):
        self.info(request)
        response_json, code = self.requester.delete_publisher(request = request, uuid = str(p_uuid))

        return Response(response_json, status = code)