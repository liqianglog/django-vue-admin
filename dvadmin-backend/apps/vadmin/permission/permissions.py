"""
常用的Permission以及DRF的Permission
@author: ruoxing
"""
import logging

from django.contrib.auth import get_user_model
from rest_framework.permissions import (BasePermission,
                                        )
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.vadmin.permission.models import Dept
from apps.vadmin.utils.model_util import get_dept

logger = logging.getLogger(__name__)
User = get_user_model()


class CustomPermission(BasePermission):
    def __init__(self, message=None) -> None:
        super().__init__()
        self.message = getattr(self.__class__, 'message', '无权限')
        self.user: User = None

    def init_permission(self, request: Request, view: APIView):
        self.user = request.user

    def has_permission(self, request: Request, view: APIView):
        return True

    def has_object_permission(self, request: Request, view: APIView, obj):
        return True


class CommonPermission(CustomPermission):
    """
    通用权限类，判断用户是否有这条数据的查询权限，如没有则直接没有操作权限
        0. 获取用户的部门id，没有部门则返回 False
        1. 判断过滤的数据是否有创建人所在部门 "dept_belong_id" 字段，没有则返回 True
        2. 如果用户没有关联角色则校验该数据是否属于本部门
        3. 根据所有角色 获取所有权限范围
            3.1 判断用户是否为超级管理员角色/如果有1(所有数据) 则有权限操作
        4. 只为仅本人数据权限时只有操作本人数据权限，并且部门为自己本部门(考虑到用户会变部门，只能看当前用户所在的部门数据)
        5. 自定数据权限 获取部门，根据部门判断，是否有权限操作
    """
    message = '没有有操作权限'

    def check_queryset(self, request, instance):
        # 0. 获取用户的部门id，没有部门则返回 False
        user_dept_id = getattr(request.user, 'dept_id')
        if not user_dept_id:
            self.message = "该用户无部门，无权限操作！"
            return False

        # 1. 判断过滤的数据是否有创建人所在部门 "dept_belong_id" 字段，没有则返回 True
        if not getattr(instance, 'dept_belong_id', None):
            return True

        # 2. 如果用户没有关联角色则校验该数据是否属于本部门
        if not hasattr(request.user, 'role'):
            self.message = "该用户无角色，无权限操作！"
            return False

        # 3. 根据所有角色 获取所有权限范围
        role_list = request.user.role.filter(status='1').values('admin', 'dataScope')
        dataScope_list = []
        for ele in role_list:
            # 3.1 判断用户是否为超级管理员角色/如果有1(所有数据) 则有权限操作
            if '1' == ele.get('dataScope') or ele.get('admin') == True:
                return True
            dataScope_list.append(ele.get('dataScope'))
        dataScope_list = list(set(dataScope_list))

        # 4. 只为仅本人数据权限时只有操作本人数据权限，并且部门为自己本部门(考虑到用户会变部门，只能看当前用户所在的部门数据)
        if dataScope_list == ['5']:
            return int(instance.dept_belong_id) == user_dept_id and request.user == instance.creator

        # 5. 自定数据权限 获取部门，根据部门判断，是否有权限操作
        dept_list = []
        for ele in dataScope_list:
            if ele == '2':
                dept_list.extend(request.user.role.filter(status='1').values_list('dept__id', flat=True))
            elif ele == '3':
                dept_list.append(user_dept_id)
            elif ele == '4':
                dept_list.extend(get_dept(user_dept_id, ))
        return int(instance.dept_belong_id) in list(set(dept_list))

    def has_permission(self, request: Request, view: APIView):
        return True

    def has_object_permission(self, request: Request, view: APIView, instance):
        self.message = f"没有此数据操作权限!"
        res = self.check_queryset(request, instance)
        return res


class DeptDestroyPermission(CustomPermission):
    """
    部门删除权限校验：判断部门下是否有用户存在，存在不可删除
    """
    message = '没有有操作权限'

    def has_permission(self, request: Request, view: APIView):
        return True

    def check_queryset(self, request, instance):
        if list(filter(None, instance.values_list('userprofile', flat=True))):
            self.message = "该部门下有关联用户，无法删除！"
            return False
        if Dept.objects.filter(parentId__in=instance).count() > 0:
            self.message = "该部门下有下级部门，请先删除下级部门！"
            return False
        return True

    def has_object_permission(self, request: Request, view: APIView, instance):
        res = self.check_queryset(request, instance)
        return res
