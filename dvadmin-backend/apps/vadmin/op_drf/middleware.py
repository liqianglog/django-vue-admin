"""
django中间件
"""

import json
import datetime
from django.utils.deprecation import MiddlewareMixin
from mongoengine import DynamicDocument, StringField, IntField, DictField, DateTimeField
from rest_framework_mongoengine.serializers import DocumentSerializer
import logging
from ..utils.decorators import exceptionHandler
from ..utils.request_util import get_request_ip, get_request_data, get_request_path
from .viewsets import CustomMongoModelViewSet
from django.conf import settings
logger = logging.getLogger(__name__)


class ApiLog(DynamicDocument):
    """
    API访问日志的Mongo模型
    """
    request_ip = StringField(verbose_name="request_ip", help_text="请求IP")
    request_username = StringField(verbose_name="request_username", help_text="请求username")
    request_method = StringField(verbose_name="request_method", help_text="请求方法")
    request_path = StringField(verbose_name="request_path", help_text="请求路径")
    request_body = DictField(verbose_name="request_body", help_text="请求参数")
    response_code = IntField(verbose_name="response_code", help_text="响应状态码")
    response_reason = StringField(verbose_name="response_reason", help_text="响应简述")
    access_time = DateTimeField(verbose_name="access_time", help_text="访问时间")


class ApiLogSerializer(DocumentSerializer):
    """
    API访问日志的Mongo序列化器
    """
    class Meta:
        model = ApiLog
        fields = '__all__'


class ApiLogModelViewSet(CustomMongoModelViewSet):
    """
    API访问日志的CRUD视图
    """
    queryset = ApiLog.objects.all()
    serializer_class = ApiLogSerializer
    search_fields = ('request_ip', 'request_username', 'request_method', 'response_reason', 'source_system')
    ordering = '-access_time'  # 默认排序


class ApiLoggingMiddleware(MiddlewareMixin):
    """
    用于记录API访问日志中间件
    """
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.enable = op_settings.get_api_log_setting().get('enable', False)
        self.methods = op_settings.get_api_log_setting().get('methods', set())

    @classmethod
    @exceptionHandler()
    def __handle_request(cls, request):
        request.request_ip = get_request_ip(request)
        request.request_data = get_request_data(request)
        request.access_time = datetime.datetime.now()

    @classmethod
    @exceptionHandler(logger=logger)
    def __handle_response(cls, request, response):
        # request_data,request_ip由PermissionInterfaceMiddleware中间件中添加的属性
        body = getattr(request, 'request_data', {})
        # 请求含有password则用*替换掉(暂时先用于所有接口的password请求参数)
        if isinstance(body, dict) and body.get('password', ''):
            body['password'] = '*' * len(body['password'])
        info = {
            'request_ip': getattr(request, 'request_ip', 'unknown'),
            'request_username': request.user.username,
            'request_method': request.method,
            'request_path': request.path,
            'request_body': body,
            'response_code': response.status_code,
            'response_reason': response.reason_phrase,
            'source_system': getattr(settings,'SOURCE_SYSTEM_NAME',None),
            'access_time': request.access_time.strftime('%Y-%m-%d %H:%M:%S'),
        }
        log = ApiLog(**info)
        log.save()

    def process_request(self, request):
        self.__handle_request(request)

    def process_response(self, request, response):
        """
        主要请求处理完之后记录
        :param request:
        :param response:
        :return:
        """
        if self.enable:
            if self.methods == 'ALL' or request.method in self.methods:
                self.__handle_response(request, response)
        return response
