import json
from collections import Iterable

from django.apps import apps
from django.apps.config import AppConfig
from django.db.models.fields import Field
from rest_framework.renderers import JSONRenderer

from apps.vadmin.permission.models import Dept


def get_primary_field(model, many=False):
    """
    获取模型的主键列对应的Field
    :param model:
    :param many:
    :return:
    """
    primary_field: Field = list(filter(lambda field: field.primary_key, model._meta.local_fields))
    if many:
        return primary_field
    return primary_field[0]


def get_primary_key_name(model, many=False):
    primary_field = get_primary_field(model=model, many=many)
    if many:
        return [field.name for field in primary_field]
    return primary_field.name


def get_business_key_name(model):
    """
    获取业务列名称
    :param model:
    :return:
    """
    return getattr(model, 'business_field_name', get_primary_key_name(model, False))


def get_business_field(model):
    """
    获取模型的业务列对应的Field
    :param model:
    :return:
    """
    business_key_name = get_business_key_name(model)
    business_field = list(filter(lambda field: field.name == business_key_name, model._meta.local_fields))
    return business_field[0]


def get_model(app_label: str = None, model_name: str = None, model_label: str = None):
    """
    根据App、Model名称获取model_class
    使用:get_model(app_label='op_cmdb', model_name='Business')
    或者:get_model(model_label='op_cmdb.Business')
    :param app_label: settings中注册的app的名称, 例如:op_cmdb, admin
    :param model_name: 某个app中模型的类名, 如:Business, host, dept(忽略大小写)
    :param model_label: 例如: op_cmdb.Business
    :return:
    """
    if model_label:
        app_label, model_name = model_label.split(".")
    app_conf: AppConfig = apps.get_app_config(app_label)
    return app_conf.get_model(model_name)


def get_dept(dept_id: int, dept_all_list=None, dept_list=None):
    """
    递归获取部门的所有下级部门
    :param dept_id: 需要获取的部门id
    :param dept_all_list: 所有部门列表
    :param dept_list: 递归部门list
    :return:
    """
    if not dept_all_list:
        dept_all_list = Dept.objects.all().values('id', 'parentId')
    if dept_list is None:
        dept_list = [dept_id]
    for ele in dept_all_list:
        if ele.get('parentId') == int(dept_id):
            dept_list.append(ele.get('id'))
            get_dept(ele.get('id'), dept_all_list, dept_list)
    return list(set(dept_list))


class ModelRelateUtils:
    """
    封装ORM模型的映射操作,例如

    """

    @classmethod
    def model_to_dict(cls, models=None, serializer=None, default=None):
        """
        ORM模型对象转化为字典
        :param models: 模型对象
        :param serializer: 模型的序列化器
        :param default:
        :return:
        """
        if default is None:
            default = {}
        if not models or not serializer:
            return default
        is_iterable = isinstance(models, Iterable) and not isinstance(models, dict)
        if is_iterable:
            return [json.loads(JSONRenderer().render(serializer(model).data)) for model in models]
        return json.loads(JSONRenderer().render(serializer(models).data))

    @classmethod
    def serializer_to_dict(cls, datas):
        """
        ORM模型对象转化为字典
        :param datas: 序列化器反序列化之后的data
        :return:
        """
        is_iterable = isinstance(datas, Iterable)
        if is_iterable:
            return [json.loads(JSONRenderer().render(data)) for data in datas]
        return json.loads(JSONRenderer().render(datas))

    @classmethod
    def executeModelRelate(cls, model, related_name, fun_name, id_list):
        """
        执行RelatedManager的add方法
        :param model: Model
        :param related_name: 映射名称
        :param fun_name: 函数名称
        :param id_list: 单个或者多个
        :return:
        """
        # 获取函数
        related_manager = getattr(model, related_name, '')
        if not related_manager:
            return 0
        return cls.executeRelatedManager(related_manager, fun_name, id_list)

    @classmethod
    def executeRelatedManager(cls, related_manager, fun_name, id_list):
        """
        执行RelatedManager的add方法
        :param related_manager: RelatedManager
        :param fun_name: RelatedManager的函数名称
        :param id_list: 单个或者多个
        :return:
        """
        # 获取函数
        fun = getattr(related_manager, fun_name, '')
        # 判断是一个函数
        if not hasattr(fun, "__call__"):
            return 0
        # 判断参数是否一个集合
        is_iterable = isinstance(id_list, Iterable) and type(id_list) != str
        if is_iterable:
            fun(*id_list)
            return len(id_list)
        else:
            fun(id_list)
            return 1

    @classmethod
    def executeRelatedManagerAddMethod(cls, related_manager, id_list):
        """
        执行RelatedManager的add方法
        :param related_manager: RelatedManager
        :param id_list: 单个或者多个
        :return:
        """
        return cls.executeRelatedManager(related_manager, 'add', id_list)

    @classmethod
    def executeRelatedManagerSetMethod(cls, related_manager, id_list):
        """
        执行RelatedManager的add方法
        :param related_manager: RelatedManager
        :param id_list: 单个或者多个
        :return:
        """
        return cls.executeRelatedManager(related_manager, 'set', id_list)

    @classmethod
    def executeRelatedManagerRemoveMethod(cls, related_manager, id_list):
        """
        执行RelatedManager的remove方法
        :param related_manager: RelatedManager
        :param id_list: 单个或者多个
        :return:
        """
        return cls.executeRelatedManager(related_manager, 'remove', id_list)
