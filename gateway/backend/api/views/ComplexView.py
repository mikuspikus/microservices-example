from rest_framework.views import APIView, Request, Response, status

import logging
from uuid import UUID

from api.requesters.ArticleRequester import ArticleRequester
from api.requesters.UserRequester import UserRequester
from api.requesters.JournalRequester import JournalRequester

from api.permissions import IsAuthenticatedByAuthenticateService

from .BaseView import BaseView

class BaseComplexView(BaseView):
    a_requester = ArticleRequester()
    u_requester = UserRequester()
    j_requester = JournalRequester()

class UserArticlesView(BaseComplexView):
    permission_classes = (IsAuthenticatedByAuthenticateService, )

    def get(self, request: Request, user_id: int) -> Response:
        self.info(request)

        u_json, code = self.u_requester.user(request = request, id_ = user_id)

        if code != 200:
            return Response(data = {'errors' : 'user not found'}, status = status.HTTP_404_NOT_FOUND)

        u_uuid = u_json['outer_uuid']

        response_json, code = self.a_requester.user_articles(request, author = u_uuid)

        return Response(response_json, status = code)

class UserJournalsView(BaseComplexView):
    permission_classes = (IsAuthenticatedByAuthenticateService, )

    def get(self, request: Request, user_id: int) -> Response:
        self.info(request)

        u_json, code = self.u_requester.user(request, id_ = user_id)

        if code != 200:
            return Response(data = {'errors' : 'user not found'}, status = status.HTTP_404_NOT_FOUND)

        u_uuid = u_json['outer_uuid']
        arts_json, code = self.a_requester.user_articles(request, author = u_uuid)

        if code != 200:
            return Response(data = {'errors' : f'articles for user : \'{u_uuid}\' not found'}, status = status.HTTP_404_NOT_FOUND)

        journals = []

        for art_json in arts_json:
            j_uuid = art_json['journal']

            journal_json, code = self.j_requester.journal(request, j_uuid)

            if code != 200:
                journal_json = {'errors' : {f'journal with uuid = \'{j_uuid}\' not found'}}

            journals.append(journal_json)

        return Response(data = journals, status = status.HTTP_200_OK)