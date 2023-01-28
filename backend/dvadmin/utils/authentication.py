import logging

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication

logger = logging.getLogger(__name__)
UserModel = get_user_model()


class CustomJWTAuthentication(JWTAuthentication):
    """
    自定义JWT 认证
    """

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)

        payload = validated_token.payload
        if payload.get('production_line_id', None):
            user.production_line_id = payload.get('production_line_id')
        if payload.get('device_id', None):
            user.device_id = payload.get('device_id')
        return user, validated_token
