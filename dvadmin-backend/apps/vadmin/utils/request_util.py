"""
Request工具类
"""
import json
import logging

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.urls.resolvers import ResolverMatch
from user_agents import parse

from application import settings
from apps.vadmin.utils.authentication import OpAuthJwtAuthentication

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
    try:
        user, tokrn = OpAuthJwtAuthentication().authenticate(request)
    except Exception as e:
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
        try:
            body = request.body
            if body:
                data = json.loads(body)
        except Exception as e:
            pass
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
        if key == 'pk':
            path = path.replace(f"/{value}", f"/{{id}}")
            continue
        path = path.replace(f"/{value}", f"/{{{key}}}")

    return path


def get_browser(request, *args, **kwargs):
    """
    获取浏览器名
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    ua_string = request.META['HTTP_USER_AGENT']
    user_agent = parse(ua_string)
    return user_agent.get_browser()


def get_os(request, *args, **kwargs):
    """
    获取操作系统
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    ua_string = request.META['HTTP_USER_AGENT']
    user_agent = parse(ua_string)
    return user_agent.get_os()


def get_login_location(request, *args, **kwargs):
    """
    获取ip 登录位置
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    if not getattr(settings, "ENABLE_LOGIN_LOCATION", False): return ""
    import requests
    import eventlet  # 导入eventlet这个模块
    request_ip = get_request_ip(request)
    # 从缓存中获取
    location = cache.get(request_ip) if getattr(settings, "REDIS_ENABLE", False) else ""
    if location:
        return location
    # 通过api 获取，再缓存redis
    try:
        eventlet.monkey_patch(thread=False)  # 必须加这条代码
        with eventlet.Timeout(2, False):  # 设置超时时间为2秒
            apiurl = "http://whois.pconline.com.cn/ip.jsp?ip=%s" % request_ip
            r = requests.get(apiurl)
            content = r.content.decode('GBK')
            location = str(content).replace('\r', '').replace('\n', '')[:64]
            if getattr(settings, "REDIS_ENABLE", False):
                cache.set(request_ip, location, 86400)
            return location
    except Exception as e:
        pass
    return ""


def get_verbose_name(queryset=None, view=None, model=None):
    """
    获取 verbose_name
    :param request:
    :param view:
    :return:
    """
    try:
        if queryset and hasattr(queryset, 'model'):
            model = queryset.model
        elif view and hasattr(view.get_queryset(), 'model'):
            model = view.get_queryset().model
        elif view and hasattr(view.get_serializer(), 'Meta') and hasattr(view.get_serializer().Meta, 'model'):
            model = view.get_serializer().Meta.model
        if model:
            return getattr(model, '_meta').verbose_name
    except Exception as e:
        pass
    return ""
