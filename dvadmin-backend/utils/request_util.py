"""
Request工具类
"""
import json
import logging
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.authentication import BaseAuthentication
from rest_framework.settings import api_settings as drf_settings
from django.contrib.auth.models import AnonymousUser
from django.urls.resolvers import ResolverMatch


logger = logging.getLogger(__name__)


def get_request_user(request, authenticate=True):
    """
    获取请求user
    (1)如果request里的user没有认证,那么则手动认证一次
    :param request:
    :param authenticate:
    :return:
    """
    user: AbstractBaseUser = getattr(request, 'user', None)
    if user and user.is_authenticated:
        return user
    authentication: BaseAuthentication = None
    for authentication_class in drf_settings.DEFAULT_AUTHENTICATION_CLASSES:
        try:
            authentication = authentication_class()
            user_auth_tuple = authentication.authenticate(request)
            if user_auth_tuple is not None:
                user, token = user_auth_tuple
                if authenticate:
                    request.user = user
                return user
        except Exception:
            pass
    return user or AnonymousUser()


def get_request_ip(request):
    """
    获取请求IP
    :param request:
    :return:
    """
    ip = getattr(request, 'request_ip', None)
    if ip:
        return ip
    ip = request.META.get('REMOTE_ADDR', '')
    if not ip:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = 'unknown'
    return ip


def get_request_data(request):
    """
    获取请求参数
    :param request:
    :return:
    """
    request_data = getattr(request, 'request_data', None)
    if request_data:
        return request_data
    data: dict = {**request.GET.dict(), **request.POST.dict()}
    if not data:
        body = getattr(request, '_body', request.body)
        if body:
            data = json.loads(body)
        if not isinstance(data, dict):
            data = {'data': data}
    return data


def get_request_path(request, *args, **kwargs):
    """
    获取请求路径
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    request_path = getattr(request, 'request_path', None)
    if request_path:
        return request_path
    values = []
    for arg in args:
        if len(arg) == 0:
            continue
        if isinstance(arg, str):
            values.append(arg)
        elif isinstance(arg, (tuple, set, list)):
            values.extend(arg)
        elif isinstance(arg, dict):
            values.extend(arg.values())
    if len(values) == 0:
        return request.path
    path: str = request.path
    for value in values:
        path = path.replace('/' + value, '/' + '{id}')
    return path


def get_request_canonical_path(request, *args, **kwargs):
    """
    获取请求路径
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    request_path = getattr(request, 'request_canonical_path', None)
    if request_path:
        return request_path
    path: str = request.path
    resolver_match: ResolverMatch = request.resolver_match
    for value in resolver_match.args:
        path = path.replace(f"/{value}", "/{id}")
    for key, value in resolver_match.kwargs.items():
        path = path.replace(f"/{value}", f"/{{{key}}}")
        if key == 'pk':
            pass
    return path
