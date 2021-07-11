"""
常用的装饰器以及DRF的装饰器
"""
import functools
import logging
import time
import traceback
from collections import Iterable
from datetime import datetime

from django.conf import settings
from django.utils import six
from django.utils.decorators import available_attrs
from rest_framework.response import Response
from rest_framework_extensions.settings import extensions_api_settings

from application.celery import app
from apps.vadmin.system.models import CeleryLog
from apps.vadmin.utils.string_util import bas64_encode_text, bas64_decode_text


def get_cache(alias=None):
    from django.core.cache import caches
    return caches[alias or extensions_api_settings.DEFAULT_USE_CACHE]


logger = logging.getLogger(__name__)


def BaseCeleryApp(name, save_success_logs=True):
    """
    celery 保存日志基础类
    :param name: celery任务名字
    :param save_success_logs: 是否保存成功的日志(适用于频率高的celery任务，成功不需要保存日志，则传False)
    :return:
    """

    def wraps(func):
        @app.task(name=name)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            obj = CeleryLog()
            obj.name = ''.join(str(func.__doc__).replace(' ', '').split('\n')[:2])
            obj.func_name = str(func.__name__)
            obj.kwargs = f"*args：{args}\n**kwargs：{kwargs}"
            start_time = datetime.now()
            res = None
            try:
                res = func(*args, **kwargs)
                if not save_success_logs:
                    return res
                obj.result = str(res)
                obj.status = True
            except Exception as exc:
                obj.status = False
                obj.result = f"执行失败，错误信息：{exc}"
                logger.info(f"传入参数:{args, kwargs}")
                logger.error(f"执行失败，错误信息：{exc}")
            end_time = datetime.now()
            seconds = (end_time - start_time).seconds
            obj.seconds = seconds
            obj.save()
            return res

        return wrapper

    return wraps


def print_fun_time(logger=None):
    """
    打印函数执行时间
    :param logger:
    :return:
    """

    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            start_time = datetime.now()
            res = func(*args, **kwargs)
            end_time = datetime.now()
            seconds = (end_time - start_time).seconds
            if logger:
                logger.info(f"{func.__name__}耗时:{seconds}秒")
            else:
                print(f"{func.__name__}耗时:{seconds}秒")
            return res

        return inner

    return wrapper


def print_time(logger=None):
    """
    打印函数执行时间
    :param logger:
    :return:
    """

    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            start_time = time.time()
            res = func(*args, **kwargs)
            end_time = time.time()
            seconds = "%.3f" % (end_time - start_time)
            if logger:
                logger.info(f"{func.__name__}耗时:{seconds}秒")
            else:
                print(f"{func.__name__}耗时:{seconds}秒")
            return res

        return inner

    return wrapper


def bas64_encode(func):
    """
    装饰器:Base64加密文本(func返回的文本)
    :param func:
    :return:
    """

    def inner(*args, **kwargs):
        text = func(*args, **kwargs)
        if isinstance(text, str):
            text = bas64_encode_text(text)
        return text

    return inner


def bas64_decode(func):
    """
    装饰器:Base64解密文本(func返回的文本)
    :param func:
    :return:
    """

    def inner(*args, **kwargs):
        text = func(*args, **kwargs)
        if isinstance(text, str):
            text = bas64_decode_text(text)
        return text

    return inner


def decode(crypto=""):
    """
    解密装饰器:BASE64
    :param crypto: 解密算法名称(忽略大小写)
    """

    def wrapper(func):
        def inner(*args, **kwargs):
            text = func(*args, **kwargs)
            if isinstance(text, str) or crypto:
                if crypto.lower() == 'base64':
                    text = bas64_decode_text(text)
                else:
                    text = text
            return text

        return inner

    return wrapper


def encode(crypto=""):
    """
    解密装饰器:BASE64
    :param crypto: 解密算法名称(忽略大小写)
    """

    def wrapper(func):
        def inner(*args, **kwargs):
            text = func(*args, **kwargs)
            return text

        return inner

    return wrapper


def envFunction(envs='', execute=True, result=None):
    """
    环境函数装饰器:根据指导环境与当前环境是否匹配,判断是否执行某个函数
    :param envs:为True时,当前环境与指定的envs匹配时,执行该函数
    :      为False时,当前环境与指定的envs匹配时,不执行该函数
    :param result:指定当该函数被越过时的返回值,默认None
    实例:当环境为production时,才会执行robot_broadcast(),否则相当于在robot_broadcast里直接return
        @envFunction(envs=['production', ], execute=True)
        def robot_broadcast(content=''):
           pass

    """

    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            environments = []
            if not envs:
                environments = []
            elif isinstance(envs, str):
                environments = [envs, ]
            elif isinstance(envs, (Iterable,)):
                environments = envs
            if settings.PROJECT_ENV in environments and execute:
                return func(*args, **kwargs)
            elif settings.PROJECT_ENV not in environments and not execute:
                return func(*args, **kwargs)
            return result

        return inner

    return wrapper


def exceptionHandler(logger=None, throw=False, result=None, message=None):
    """
    异常装饰器:用于统一处理捕获的异常
    :param logger: 指定Logger
    :param throw: 继续抛出这个异常
    :param result: 发生异常时的返回值(throw=True时,无效)
    :param message: 错误信息
    :return:
    """

    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if logger:
                    logger.error(traceback.format_exc())
                if message:
                    logger.error(message)
                if throw:
                    raise e
                return result

        return inner

    return wrapper


class CacheResponse(object):
    def __init__(self,
                 timeout=None,
                 key_func=None,
                 cache=None,
                 cache_errors=None):
        if timeout is None:
            self.timeout = extensions_api_settings.DEFAULT_CACHE_RESPONSE_TIMEOUT
        else:
            self.timeout = timeout

        if key_func is None:
            self.key_func = 'get_cache_key'
        else:
            self.key_func = key_func

        if cache_errors is None:
            self.cache_errors = extensions_api_settings.DEFAULT_CACHE_ERRORS
        else:
            self.cache_errors = cache_errors

        self.cache = get_cache(cache or extensions_api_settings.DEFAULT_USE_CACHE)

    def __call__(self, func):
        this = self

        @functools.wraps(func, assigned=available_attrs(func))
        def inner(self, request, *args, **kwargs):
            return this.process_cache_response(
                view_instance=self,
                view_method=func,
                request=request,
                args=args,
                kwargs=kwargs,
            )

        return inner

    def process_cache_response(self,
                               view_instance,
                               view_method,
                               request,
                               args,
                               kwargs):
        key = self.calculate_key(
            view_instance=view_instance,
            view_method=view_method,
            request=request,
            args=args,
            kwargs=kwargs
        )
        is_no_cache = False
        is_no_cache_fun = getattr(view_instance, 'is_no_cache', None)
        if is_no_cache_fun and is_no_cache_fun(request):
            is_no_cache = True
        response = None
        if not is_no_cache:
            response = self.cache.get(key)  if getattr(settings, "REDIS_ENABLE", False) else None
        if not response:
            response = view_method(view_instance, request, *args, **kwargs)
            response = view_instance.finalize_response(request, response, *args, **kwargs)
            response.render()  # should be rendered, before picklining while storing to cache

            if not response.status_code >= 400 or self.cache_errors:
                if not is_no_cache:
                    if getattr(settings, "REDIS_ENABLE", False):
                        if isinstance(response, Response):
                            self.cache.set(key, response.data, self.timeout)
                        else:
                            self.cache.set(key, response, self.timeout)
                    handle_refresh_cache_fun = getattr(view_instance, 'handle_refresh_cache', None)
                    if handle_refresh_cache_fun:
                        handle_refresh_cache_fun(request=request, key=key, cache=self.cache)
        if not isinstance(response, Response):
            response = Response(data=response)
        if not hasattr(response, '_closable_objects'):
            response._closable_objects = []
        return response

    def calculate_key(self,
                      view_instance,
                      view_method,
                      request,
                      args,
                      kwargs):
        if isinstance(self.key_func, six.string_types):
            key_func = getattr(view_instance, self.key_func)
        else:
            key_func = self.key_func
        return key_func(
            view_instance=view_instance,
            view_method=view_method,
            request=request,
            args=args,
            kwargs=kwargs,
        )


cache_response = CacheResponse
