from datetime import timedelta
from uuid import uuid4

import rest_framework_simplejwt
from django.conf import settings as django_setting
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.module_loading import import_string

from rest_framework_simplejwt.exceptions import TokenBackendError, TokenError
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import Token, BlacklistMixin
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.utils import (
    aware_utcnow, datetime_from_epoch, datetime_to_epoch, format_lazy,
)

from common.drf.response import Response


class AccessToken(BlacklistMixin, Token):
    token_type = 'access'
    lifetime = api_settings.ACCESS_TOKEN_LIFETIME
    no_copy_claims = (
        api_settings.TOKEN_TYPE_CLAIM,
        'exp',

        # Both of these claims are included even though they may be the same.
        # It seems possible that a third party token might have a custom or
        # namespaced JTI claim as well as a default "jti" claim.  In that case,
        # we wouldn't want to copy either one.
        api_settings.JTI_CLAIM,
        'jti',
    )

    def blacklist(self):
        """
        Ensures this token is included in the outstanding token list and
        adds it to the blacklist.
        """
        jti = self.payload[api_settings.JTI_CLAIM]
        exp = self.payload['exp']
        user_id_field = api_settings.USER_ID_FIELD
        user_kwargs = {
            user_id_field: self.payload['user_id']
        }
        user_id = get_user_model().objects.get(**user_kwargs)
        # Ensure outstanding token exists with given jti
        token, _ = OutstandingToken.objects.get_or_create(
            jti=jti,
            user=user_id,
            # created_at=token.current_time,
            defaults={
                'token': str(self),
                'expires_at': datetime_from_epoch(exp),
            },
        )
        return BlacklistedToken.objects.get_or_create(token=token)


from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework import permissions, status


class LogoutAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # def delete(self, request):
    #     # find all tokens by user and blacklists them, forcing them to log out.
    #     try:
    #         tokens = OutstandingToken.objects.filter(user=request.user)
    #         for token in tokens:
    #             token = RefreshToken(token.token)
    #             token.blacklist()
    #     except:
    #         token = RefreshToken(request.data.refresh_token)
    #         token.blacklist()
    #     return Response(status=status.HTTP_205_RESET_CONTENT)  # 204 means no content, 205 means no content and refresh

    def post(self, request):
        # Post is for logging out in current browser
        try:
            # refresh_token = request.data["refresh_token"]
            access = request.auth.token
            t = AccessToken(access)
            t.blacklist()
            return Response(success=True, status=status.HTTP_200_OK)
        except rest_framework_simplejwt.exceptions.TokenError as e:
            return Response(success=False, message="Token 无效！")
        except Exception:

            return Response(success=False, status=status.HTTP_400_BAD_REQUEST)
