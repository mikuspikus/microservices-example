
from rest_framework.permissions import BasePermission

class IsAuthenticatedByToken(BasePermission):

    def has_permission(self, request, view):
        return request.auth is not None