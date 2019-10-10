from rest_framework.views import APIView, Request, Response

import logging
from uuid import UUID

from api.requesters.PublisherRequester import PublisherRequester
from api.permissions import IsAuthenticatedByAuthenticateService

class BasePublisherView(APIView):
    requester = PublisherRequester()
    logger = logging.getLogger(name = 'gateway.api.views')

class PublishersView(BasePublisherView):
    permission_classes = (IsAuthenticatedByAuthenticateService, )

    def get(self, request: Request) -> Response:
        response_json, code = self.requester.publishers(request = request)

        return Response(response_json, status = code)

    def post(self, request: Request) -> Response:
        response_json, code = self.requester.post_publisher(request = request, data = request.data)

        return Response(response_json, status = code)

class PublisherView(BasePublisherView):
    permission_classes = (IsAuthenticatedByAuthenticateService, )

    def get(self, request: Request, p_uuid: UUID):
        response_json, code = self.requester.publisher(request = request, uuid = str(p_uuid))

        return Response(response_json, status = code)
    
    def patch(self, request: Request, p_uuid: UUID):
        response_json, code = self.requester.patch_publisher(request = request, data = request.data, uuid = str(p_uuid))

        return Response(response_json, status = code)

    def delete(self, request: Request, p_uuid: UUID):
        response_json, code = self.requester.delete_publisher(request = request, uuid = str(p_uuid))

        return Response(response_json, status = code)