"""
django中间件
"""
import json
import logging
import os

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from apps.vadmin.op_drf.response import ErrorJsonResponse
from apps.vadmin.permission.models import Menu
from apps.vadmin.system.models import OperationLog
from apps.vadmin.utils.request_util import get_request_ip, get_request_data, get_request_path, get_browser, get_os, \
    get_login_location, get_request_canonical_path, get_request_user, get_verbose_name

logger = logging.getLogger(__name__)


class ApiLoggingMiddleware(MiddlewareMixin):
    """
    用于记录API访问日志中间件
    """

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.enable = getattr(settings, 'API_LOG_ENABLE', None) or False
        self.methods = getattr(settings, 'API_LOG_METHODS', None) or set()

    @classmethod
    def __handle_request(cls, request):
        request.request_ip = get_request_ip(request)
        request.request_data = get_request_data(request)
        request.request_path = get_request_path(request)

    @classmethod
    def __handle_response(cls, request, response):
        # request_data,request_ip由PermissionInterfaceMiddleware中间件中添加的属性
        body = getattr(request, 'request_data', {})
        # 请求含有password则用*替换掉(暂时先用于所有接口的password请求参数)
        if isinstance(body, dict) and body.get('password', ''):
            body['password'] = '*' * len(body['password'])
        if not hasattr(response, 'data') or not isinstance(response.data, dict):
            response.data = {}
        if not response.data and response.content:
            try:
                content = json.loads(response.content.decode())
                response.data = content if isinstance(content, dict) else {}
            except:
                pass
        user = get_request_user(request)
        info = {
            'request_ip': getattr(request, 'request_ip', 'unknown'),
            'creator': user if not isinstance(user, AnonymousUser) else None,
            'dept_belong_id': getattr(request.user, 'dept_id', None),
            'request_method': request.method,
            'request_path': request.request_path,
            'request_body': body,
            'response_code': response.data.get('code'),
            'request_location': get_login_location(request),
            'request_os': get_os(request),
            'request_browser': get_browser(request),
            'request_msg': request.session.get('request_msg'),
            'status': True if response.data.get('code') in [200, 204] else False,
            'json_result': {"code": response.data.get('code'), "msg": response.data.get('msg')},
            'request_modular': request.session.get('model_name'),
        }
        log = OperationLog(**info)
        log.save()

    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(view_func, 'cls') and hasattr(view_func.cls, 'queryset'):
            request.session['model_name'] = get_verbose_name(view_func.cls.queryset)
        return

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


class PermissionModeMiddleware(MiddlewareMixin):
    """
    权限模式拦截判断
    """

    def process_request(self, request):
        return

    def has_interface_permission(self, request, method, view_path, user=None):
        """
        接口权限验证,优先级:
        (1)接口是否接入权限管理, 是:继续; 否:通过
        (2)认证的user是否superuser, 是:通过; 否:继续
        (3)user的角色有该接口权限, 是:通过, 否:不通过

        auth_code含义: auth_code >=0, 表示接口认证通过; auth_code < 0, 表示无接口访问权限, 具体含义如下
         -1:
         -10: 该请求已认证的用户没有这个接口的访问权限
           0:
           1: 白名单
          10: 该接口没有录入权限系统, 放行 请求中认证的用户为超级管理员, 直接放行
          20: 请求中认证的用户是superuser放行
          30: 请求中认证的用户对应的角色中,某个角色包含了该接口的访问权限, 放行
        1. 先获取所有录入系统的接口
        2  判断此用户是否为 superuser
        3. 获取此用户所请求的接口
        4. 获取此用户关联角色所有有权限的接口

        :param interface: 接口模型
        :param path: 接口路径
        :param method: 请求方法
        :param project: 接口所属项目
        :param args:
        :param kwargs:
        :return:
        """
        interface_dict = Menu.get_interface_dict()
        # (1) 接口是否接入权限管理, 是:继续; 否:通过
        if not view_path in interface_dict.get(method, []):
            return 10
        # (2)认证的user是否superuser, 是:通过; 否:继续
        if user.is_superuser or (hasattr(user, 'role') and user.role.filter(status='1', admin=True).count()):
            return 20
        # (3)user的角色有该接口权限, 是:通过, 否:不通过
        if view_path in user.get_user_interface_dict.get(method, []):
            return 30
        return -10

    def process_view(self, request, view_func, view_args, view_kwargs):
        # 判断环境变量中，是否为演示模式(正常可忽略此判断)
        white_list = ['/admin/logout/', '/admin/login/', '/admin/api-auth/login/']
        if os.getenv('DEMO_ENV') and not request.method in ['GET', 'OPTIONS'] and request.path not in white_list:
            return ErrorJsonResponse(data={}, msg=f'演示模式，不允许操作!')

        if not settings.INTERFACE_PERMISSION:
            return
        user = get_request_user(request)

        if user and not isinstance(user, AnonymousUser):
            method = request.method.upper()
            if method == 'GET':  # GET 不设置接口权限
                return
            view_path = get_request_canonical_path(request, *view_args, **view_kwargs)
            auth_code = self.has_interface_permission(request, method, view_path, user)
            logger.info(f"[{user.username}] {method}:{view_path}, 权限认证:{auth_code}")
            if auth_code >= 0:
                return
            return ErrorJsonResponse(data={}, msg=f'无接口访问权限!')

    def process_response(self, request, response):
        """
        主要请求处理完之后记录
        :param request:
        :param response:
        :return:
        """
        return response
