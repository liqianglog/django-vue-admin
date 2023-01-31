# 自定义权限
import re

from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission


class DeviceManagePermission(BasePermission):
    """
    设备管理权限
    """

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        # 判断是否是超级管理员
        if request.user.is_superuser:
            return True
        # 判断用户类型是否是2 设备用户
        if request.user.user_type == 2:
            return True
