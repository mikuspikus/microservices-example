from .BaseView import BaseView
from rest_framework.views import APIView, Request, Response, status
from rest_framework.renderers import TemplateHTMLRenderer

from django.contrib.auth import logout
from django.shortcuts import redirect

class HomeView(BaseView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/generic/index.html'

    def get(self, request: Request) -> Response:
        return Response()

class LogoutView(BaseView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request: Request) -> Response:
        # logout(request)
        response = redirect('index')
        response.delete_cookie('Authorization')

        return response