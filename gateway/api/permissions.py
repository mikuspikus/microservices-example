from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from api.requesters import UserRequester

class IsAuthenticatedByAuthenticateService(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        _, code = UserRequester().info(request = request)
        return code == 200