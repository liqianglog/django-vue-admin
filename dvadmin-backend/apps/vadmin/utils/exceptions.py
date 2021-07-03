import logging
import traceback

from rest_framework import exceptions
from rest_framework.views import set_rollback

from apps.vadmin.op_drf.response import ErrorResponse

logger = logging.getLogger(__name__)

from rest_framework.exceptions import APIException as DRFAPIException, AuthenticationFailed


class APIException(Exception):
    """
    通用异常:(1)用于接口请求是抛出移除, 此时code会被当做标准返回的code, message会被当做标准返回的msg
    """

    def __init__(self, code=201, message='API异常', args=('API异常',)):
        self.args = args
        self.code = code
        self.message = message

    def __str__(self):
        return self.message


class GenException(APIException):
    pass


class FrameworkException(Exception):
    """
    框架异常、配置异常等
    """

    def __init__(self, message='框架异常', *args: object, **kwargs: object) -> None:
        super().__init__(*args, )
        self.message = message

    def __str__(self) -> str:
        return f"{self.message}"


class JWTAuthenticationFailedException(APIException):
    """
    JWT认证异常
    """

    def __init__(self, code=201, message=None, args=('异常',)):
        if not message:
            message = 'JWT authentication failed!'
        super().__init__(code, message, args)


def op_exception_handler(ex, context):
    """
    统一异常拦截处理
    目的:(1)取消所有的500异常响应,统一响应为标准错误返回
        (2)准确显示错误信息
    :param ex:
    :param context:
    :return:
    """
    msg = ''
    code = '201'

    if isinstance(ex, AuthenticationFailed):
        code = 401
        msg = ex.detail
    elif isinstance(ex, DRFAPIException):
        set_rollback()
        msg = ex.detail
    elif isinstance(ex, exceptions.APIException):
        set_rollback()
        msg = ex.detail
    elif isinstance(ex, Exception):
        logger.error(traceback.format_exc())
        msg = str(ex)
    return ErrorResponse(msg=msg, code=code)
