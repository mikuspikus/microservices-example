from .models import GatewayUser
from .requesters.UserRequester import UserRequester

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import Request

from typing import Union, Tuple

class CookieTokenAuthentication(BaseAuthentication):

    def authenticate(self, request: Request) -> Union[None, Tuple[GatewayUser, str]]:
        token = request.META.get('HTTP_AUTHORIZATION')

        if not token:
            return None

        credentials, code = UserRequester().info(request)

        if code == 404:
            raise AuthenticationFailed('Authentication sevice is unavailable')

        if code != 200:
            raise AuthenticationFailed('Cannot authenticate user')

        try:
            user = GatewayUser.objects.get(identifier = credentials['id'])

        except GatewayUser.DoesNotExist:
            user = GatewayUser(
                username = credentials['username'],
                identifier = credentials['id'],
                outer_uuid = credentials['uuid']
            )

            user.save()

        return (user, token)

class DjangoAuthentication:
    def authenticate(self, request = None, username=None, identifier=None, token=None, uuid=None):
        try:
            user = GatewayUser.objects.get(identifier = identifier)

        except GatewayUser.DoesNotExist:
            user = GatewayUser(
                username = username,
                identifier = identifier,
                token = token,
                outer_uuid = uuid
            )

            user.save()

        return user

    def get_user(self, user_id):
        try:
            return GatewayUser.objects.get(pk = user_id)

        except GatewayUser.DoesNotExist:
            return None
'''
class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request: Request) -> Union[None, Tuple[GatewayUser, str]]:
        credentials, code = UserRequester().authenticate(request.data)

        if code != 200:
            return None

        user = GatewayUser.objects.get_or_create(
            username = credentials['username'],
            token = credentials['token'],
            identidier = credentials['user_id'],
            outer_uuid = credentials['uuid']
        )

        return (user, credentials['token'])

        token = request.META.get('HTTP_AUTHORIZATION')

        if not token:
            return None

        user_data, code = UserRequester().info(request)

        if code != 200:
            raise AuthenticationFailed('Invalid user token')

        user = GatewayUser.objects.get_or_create(
            username = user_data['username'],
            token = user_data['token'],
            identidier = user_data['user_id'],
            outer_uuid = user_data['uuid']
        )

        return (user, user_data['token'])
'''


