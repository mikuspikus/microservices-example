from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated

from datetime import timedelta
from django.utils import timezone
from django.conf import settings

from typing import Tuple

from .models import CustomToken


def expires_in(token: CustomToken) -> int:
    time_elapsed = timezone.now() - token.created
    time_left = timedelta(
        seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    return time_left


def is_token_expired(token: CustomToken) -> bool:
    return expires_in(token) < timedelta(seconds=0)


def token_handler(token: CustomToken) -> Tuple[bool, CustomToken]:
    is_expired = is_token_expired(token)

    # if is_expired:
    #     token.generate_token()
    #     token.save()

    return (is_expired, token)


class ExpiringTokenAuthentication(TokenAuthentication):
    model = CustomToken
    keyword = 'Bearer'

    def authenticate_credentials(self, token):
        model = self.model
        try:
            token_ = model.objects.get(token=token)

        except model.DoesNotExist:
            msg = 'Invalid token'
            raise AuthenticationFailed(msg)

        is_expired, token_ = token_handler(token_)

        if is_expired:
            msg = 'Token has expired'
            raise NotAuthenticated(msg)

        return (None, token_)
