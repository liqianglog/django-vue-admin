"""
常用的过滤器以及DRF的过滤器
"""
import json
import logging
import operator
from functools import reduce

from django.utils import six
from mongoengine.queryset import visitor
from rest_framework.filters import BaseFilterBackend, SearchFilter, OrderingFilter

from apps.vadmin.utils.model_util import get_dept

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
    0. 获取用户的部门id，没有部门则返回空
    1. 判断过滤的数据是否有创建人所在部门 "creator" 字段,没有则返回全部
    2. 如果用户没有关联角色则返回本部门数据
    3. 根据角色的最大权限进行数据过滤(会有多个角色，进行去重取最大权限)
    3.1 判断用户是否为超级管理员角色/如果有1(所有数据) 则返回所有数据

    4. 只为仅本人数据权限时只返回过滤本人数据，并且部门为自己本部门(考虑到用户会变部门，只能看当前用户所在的部门数据)
    5. 自定数据权限 获取部门，根据部门过滤
    """

    def filter_queryset(self, request, queryset, view):
        # 0. 获取用户的部门id，没有部门则返回空
        user_dept_id = getattr(request.user, 'dept_id')
        if not user_dept_id:
            return queryset.none()

        # 1. 判断过滤的数据是否有创建人所在部门 "dept_belong_id" 字段
        if not getattr(queryset.model, 'dept_belong_id', None):
            return queryset

        # 2. 如果用户没有关联角色则返回本部门数据
        if not hasattr(request.user, 'role'):
            return queryset.filter(dept_belong_id=user_dept_id)

        # 3. 根据所有角色 获取所有权限范围
        role_list = request.user.role.filter(status='1').values('admin', 'dataScope')
        dataScope_list = []
        for ele in role_list:
            # 3.1 判断用户是否为超级管理员角色/如果有1(所有数据) 则返回所有数据
            if '1' == ele.get('dataScope') or ele.get('admin') == True:
                return queryset
            dataScope_list.append(ele.get('dataScope'))
        dataScope_list = list(set(dataScope_list))

        # 4. 只为仅本人数据权限时只返回过滤本人数据，并且部门为自己本部门(考虑到用户会变部门，只能看当前用户所在的部门数据)
        if dataScope_list == ['5']:
            return queryset.filter(creator=request.user, dept_belong_id=user_dept_id)

        # 5. 自定数据权限 获取部门，根据部门过滤
        dept_list = []
        for ele in dataScope_list:
            if ele == '2':
                dept_list.extend(request.user.role.filter(status='1').values_list('dept__id', flat=True))
            elif ele == '3':
                dept_list.append(user_dept_id)
            elif ele == '4':
                dept_list.extend(get_dept(user_dept_id, ))
        return queryset.filter(dept_belong_id__in=list(set(dept_list)))
