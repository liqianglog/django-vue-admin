import datetime
import logging
from uuid import uuid4

from captcha.models import CaptchaStore
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken, jwt_response_payload_handler

from apps.vadmin.system.models.logininfor import LoginInfor
from apps.vadmin.utils.exceptions import GenException
from apps.vadmin.utils.jwt_util import jwt_get_session_id
from apps.vadmin.utils.request_util import get_request_ip, get_os, get_browser, get_login_location
from apps.vadmin.op_drf.response import SuccessResponse, ErrorResponse

logger = logging.getLogger(__name__)

User = get_user_model()


class LogoutView(APIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    prefix = settings.JWT_AUTH.get('JWT_AUTH_HEADER_PREFIX', 'JWT')

    def post(self, request):
        user = request.user
        user.user_secret = uuid4()
        user.save()
        key = f"{self.prefix}_{user.username}"
        if getattr(settings, "REDIS_ENABLE", False):
            cache.delete(key)
        return SuccessResponse()


class LoginView(ObtainJSONWebToken):
    JWT_AUTH_COOKIE = ''
    prefix = settings.JWT_AUTH.get('JWT_AUTH_HEADER_PREFIX')
    ex = settings.JWT_AUTH.get('JWT_EXPIRATION_DELTA')

    def jarge_captcha(self, request):
        """
        校验验证码
        :param request:
        :return:
        """
        if not settings.CAPTCHA_STATE:  # 未开启验证码则返回 True
            return True
        idKeyC = request.data.get('idKeyC', None)
        idValueC = request.data.get('idValueC', None)
        if not idValueC:
            raise GenException(message='请输入验证码')
        try:
            get_captcha = CaptchaStore.objects.get(hashkey=idKeyC)
            if str(get_captcha.response).lower() == idValueC.lower():  # 如果验证码匹配
                get_captcha.delete()
                return True
        except:
            pass
        else:
            if get_captcha: get_captcha.delete()
            raise GenException(message='验证码错误')

    def save_login_infor(self, request, msg='', status=True, session_id=''):
        User = get_user_model()
        instance = LoginInfor()
        instance.session_id = session_id
        instance.browser = get_browser(request)
        instance.ipaddr = get_request_ip(request)
        instance.loginLocation = get_login_location(request)
        instance.msg = msg
        instance.os = get_os(request)
        instance.status = status
        instance.creator = request.user and User.objects.filter(username=request.data.get('username')).first()
        instance.save()

    def post(self, request, *args, **kwargs):
        # 校验验证码
        self.jarge_captcha(request)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = SuccessResponse(response_data)
            if token:
                username = user.username
                session_id = jwt_get_session_id(token)
                key = f"{self.prefix}_{session_id}_{username}"
                if getattr(settings, "REDIS_ENABLE", False):
                    cache.set(key, token, self.ex.total_seconds())
                self.save_login_infor(request, '登录成功', session_id=session_id)
            if self.JWT_AUTH_COOKIE and token:
                expiration = (datetime.datetime.utcnow() + self.ex)
                response.set_cookie(self.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    domain=settings.SESSION_COOKIE_DOMAIN,
                                    httponly=False)
            return response
        self.save_login_infor(request, '登录失败，账户/密码不正确', False)
        return ErrorResponse(data=serializer.errors, msg='账户/密码不正确')

    # def handle_exception(self, exc):
    #     print(exc)
    #     return ErrorResponse(data=None, msg=exc.message)
