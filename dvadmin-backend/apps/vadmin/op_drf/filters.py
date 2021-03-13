"""
常用的过滤器以及DRF的过滤器
"""
import json
import logging
import operator
from functools import reduce

from django.db.models import Q
from django.utils import six
from mongoengine.queryset import visitor
from rest_framework.filters import BaseFilterBackend, SearchFilter, OrderingFilter

from ..permission.models import Dept

logger = logging.getLogger(__name__)


def get_as_kwargs(request):
    params = request.GET.dict()
    if 'as' not in params:
        return {}
    as_params = json.loads(params.get('as', '{}'))
    return as_params


class MongoSearchFilter(SearchFilter):
    """
    适配Mongo模型视图的Search过滤器
    """

    def filter_queryset(self, request, queryset, view):
        search_fields = getattr(view, 'search_fields', None)
        search_terms = self.get_search_terms(request)
        if not search_fields or not search_terms:
            return queryset
        orm_lookups = [
            self.construct_search(six.text_type(search_field))
            for search_field in search_fields
        ]
        if not orm_lookups:
            return queryset
        conditions = []
        for search_term in search_terms:
            queries = [
                visitor.Q(**{orm_lookup: search_term})
                for orm_lookup in orm_lookups
            ]
            conditions.append(reduce(operator.or_, queries))
        queryset = queryset.filter(reduce(operator.and_, conditions))
        return queryset


class MongoOrderingFilter(OrderingFilter):
    """
    适配Mongo模型视图的Search过滤器
    """

    def get_valid_fields(self, queryset, view, context={}):
        valid_fields = getattr(view, 'ordering_fields', self.ordering_fields)
        if valid_fields is None:
            return self.get_default_valid_fields(queryset, view, context)
        elif valid_fields == '__all__':
            # View explicitly allows filtering on any model field
            model = view.get_serializer().__class__.Meta.model
            valid_fields = [
                (field_name, getattr(field, 'verbose_name', field_name)) for field_name, field in model._fields.items()
            ]
        else:
            valid_fields = [
                (item, item) if isinstance(item, six.string_types) else item
                for item in valid_fields
            ]

        return valid_fields


class AdvancedSearchFilter(BaseFilterBackend):
    """
    高级搜索过滤器
    """

    def filter_queryset(self, request, queryset, view):
        as_kwargs = get_as_kwargs(request)
        if as_kwargs:
            queryset = queryset.filter(**as_kwargs)
        return queryset


class MongoAdvancedSearchFilter(BaseFilterBackend):
    """
    mongo高级搜索过滤器
    """

    def filter_queryset(self, request, queryset, view):
        as_kwargs = get_as_kwargs(request)
        if as_kwargs:
            queryset = queryset.filter(**as_kwargs)
        return queryset


class DataLevelPermissionsFilter(BaseFilterBackend):
    """
    数据 级权限过滤器
    0. 判断过滤的数据是否有创建人 "creator" 字段
    1. 判断用户是否为超级管理员角色
    2. 根据角色的最大权限进行数据过滤(会有多个角色，进行去重取最大权限)
    3. 只为仅本人数据权限时只返回过滤本人数据
    4. 自定数据权限 获取部门，根据部门过滤
    """
    project_resource_name: str = 'project__tenant__managers'

    def filter_queryset(self, request, queryset, view):
        # 0. 判断过滤的数据是否有创建人 "creator" 字段
        if not hasattr(queryset.model, 'creator'):
            return queryset
        # 1. 判断用户是否为超级管理员角色
        if not hasattr(request.user, 'role'):
            return queryset.filter(creator=request.user)
        role_list = request.user.role.all().values('id', 'admin', 'dataScope')
        if True in list(set([ele.get('admin') for ele in role_list])):
            return queryset

        # 2. 根据角色的最大权限进行数据过滤(会有多个角色，进行去重取最大权限)
        dataScope_list = list(set([ele.get('dataScope') for ele in role_list]))
        if '1' in dataScope_list:  # 返回所有数据
            return queryset

        # 3. 只为仅本人数据权限时只返回过滤本人数据
        if dataScope_list == ['5']:
            return queryset.filter(Q(creator=request.user))

        # 4. 自定数据权限 获取部门，根据部门过滤
        dept_list = []
        for ele in dataScope_list:
            if ele == '2':
                dept_list.extend(request.user.role.all().values_list('dept__id', flat=True))
            elif ele == '3':
                dept_list.append(request.user.dept.id)
            elif ele == '4':
                dept_list.extend(self.get_dept(request.user.dept.id, Dept.objects.all().values('id', 'parentId')))
                dept_list.append(request.user.dept.id)
        return queryset.filter(Q(creator=request.user) | Q(creator__dept__in=list(set(dept_list))))

    def get_dept(self, id, dept_all_list, dept_list=[]):
        """
        获取部门的所有下级部门
        :param id:
        :return:
        """
        for ele in dept_all_list:
            if ele.get('parentId') == id:
                dept_list.append(ele.get('id'))
                self.get_dept(ele.get('id'), dept_all_list, dept_list)
        return dept_list
