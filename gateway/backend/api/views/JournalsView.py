from rest_framework.views import APIView, Request, Response
from rest_framework.renderers import TemplateHTMLRenderer

import logging
from uuid import UUID

from api.requesters.JournalRequester import JournalRequester
from api.permissions import IsAuthenticatedByAuthenticateService

from .BaseView import BaseView

class BaseJournalView(BaseView):
    requester = JournalRequester()

class JournalsView(BaseJournalView):
    #permission_classes = (IsAuthenticatedByAuthenticateService, )

    def get(self, request: Request) -> Response:
        self.info(request)
        response_json, code = self.requester.journals(request = request)

        return Response(response_json, status = code)

    def post(self, request: Request) -> Response:
        self.info(request)
        response_json, code = self.requester.post_journal(request = request, data = request.data)

        return Response(response_json, status = code)

class JournalView(BaseJournalView):
    #permission_classes = (IsAuthenticatedByAuthenticateService, )

    def get(self, request: Request, j_uuid: UUID):
        self.info(request)
        response_json, code = self.requester.journal(request = request, uuid = str(j_uuid))

        return Response(response_json, status = code)
    
    def patch(self, request: Request, j_uuid: UUID):
        self.info(request)
        response_json, code = self.requester.patch_journal(request = request, data = request.data, uuid = str(j_uuid))

        return Response(response_json, status = code)

    def delete(self, request: Request, j_uuid: UUID):
        self.info(request)
        response_json, code = self.requester.delete_journal(request = request, uuid = str(j_uuid))

        return Response(response_json, status = code)