"""
常用的认证以及DRF的认证
"""
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils.six import text_type
from rest_framework_jwt.utils import jwt_decode_handler

from .decorators import exceptionHandler

logger = logging.getLogger(__name__)
User = get_user_model()


class OpAuthJwtAuthentication(object):
    """
    统一JWT认证(环境允许情况下, 推荐使用RedisOpAuthJwtAuthentication)
    """

    @exceptionHandler()
    def authenticate(self, request):
        token = self.get_header_authorization(request) or self.get_cookie_authorization(request)
        if not token:
            return None
        payload = jwt_decode_handler(token)
        username = payload.get('username', None)
        if not username:
            return None
        username_field = settings.USERNAME_FIELD or 'username'
        user = User.objects.filter(**{username_field: username}).first()
        if not user or not user.is_active:
            return None
        return user, token

    def authenticate_header(self, request):
        pass

    @classmethod
    def get_header_authorization(cls, request):
        """
        获取header里的认证信息, 通常用于跨域携带请求
        :param request:
        :return:
        """
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        if isinstance(auth, text_type):
            auth = auth.encode(settings.JWT_AUTH.get('HTTP_HEADER_ENCODING', 'iso-8859-1'))
        if not auth:
            return ''
        auth = str(auth, encoding='utf-8').split()
        if len(auth) != 2 or auth[0].upper() != settings.JWT_AUTH.get('JWT_AUTH_HEADER_PREFIX', 'JWT'):
            return ''
        return auth[1]

    @classmethod
    def get_cookie_authorization(cls, request):
        """
        获取cookie里JWT认证信息
        :param request:
        :return:
        """
        auth = request.COOKIES.get(settings.JWT_AUTH.get('JWT_AUTH_COOKIE', 'AUTH_JWT'), '')
        auth = auth.split()
        if len(auth) != 2 or auth[0].upper() != settings.JWT_AUTH.get('JWT_AUTH_HEADER_PREFIX', 'JWT'):
            return ''
        return auth[1]


class RedisOpAuthJwtAuthentication(OpAuthJwtAuthentication):
    """
    基于Redis的统一JWT认证(推荐使用)
    """
    prefix = settings.JWT_AUTH.get('JWT_AUTH_HEADER_PREFIX', 'JWT')

    @exceptionHandler()
    def authenticate(self, request):
        res = super().authenticate(request)
        if res:
            user, token = super().authenticate(request)
            key = f"{self.prefix}_{user.username}"
            redis_token = cache.get(key)
            if redis_token == token:
                return user, token
            else:
                return None
        return None
