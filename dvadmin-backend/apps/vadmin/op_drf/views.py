import logging
import traceback
from types import FunctionType, MethodType

from rest_framework.exceptions import APIException as DRFAPIException
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.vadmin.utils import exceptions
from .response import ErrorResponse

logger = logging.getLogger(__name__)


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
    if isinstance(ex, DRFAPIException):
        # set_rollback()
        msg = ex.detail
    elif isinstance(ex, exceptions.APIException):
        msg = ex.message
    elif isinstance(ex, Exception):
        logger.error(traceback.format_exc())
        msg = str(ex)
    return ErrorResponse(msg=msg)


class CustomAPIView(APIView):
    """
    继承、增强DRF的APIView
    """
    extra_permission_classes = ()
    # 仅当GET方法时会触发该权限的校验
    GET_permission_classes = ()

    # 仅当POST方法时会触发该权限的校验
    POST_permission_classes = ()

    # 仅当DELETE方法时会触发该权限的校验
    DELETE_permission_classes = ()

    # 仅当PUT方法时会触发该权限的校验
    PUT_permission_classes = ()

    view_logger_classes = ()

    def initial(self, request: Request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.check_extra_permissions(request)
        self.check_method_extra_permissions(request)

    def get_view_loggers(self, request: Request, *args, **kwargs):
        logger_classes = self.view_logger_classes or []
        if not logger_classes:
            return []
        view_loggers = [logger_class(view=self, request=request, *args, **kwargs) for logger_class in logger_classes]
        return view_loggers

    def handle_logging(self, request: Request, *args, **kwargs):
        view_loggers = self.get_view_loggers(request, *args, **kwargs)
        method = request.method.lower()
        for view_logger in view_loggers:
            view_logger.handle(request, *args, **kwargs)
            logger_fun = getattr(view_logger, f'handle_{method}', f'handle_other')
            if logger_fun and isinstance(logger_fun, (FunctionType, MethodType)):
                logger_fun(request, *args, **kwargs)

    def get_extra_permissions(self):
        return [permission() for permission in self.extra_permission_classes]

    def check_extra_permissions(self, request: Request):
        for permission in self.get_extra_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )

    def get_method_extra_permissions(self):
        _name = self.request.method.upper()
        method_extra_permission_classes = getattr(self, f"{_name}_permission_classes", None)
        if not method_extra_permission_classes:
            return []
        return [permission() for permission in method_extra_permission_classes]

    def check_method_extra_permissions(self, request):
        for permission in self.get_method_extra_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(
                    request, message=getattr(permission, 'message', None)
                )
