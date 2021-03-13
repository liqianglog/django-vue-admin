import django_filters

from ..permission.models import Menu, Dept, Post, Role, UserProfile


class MenuFilter(django_filters.rest_framework.FilterSet):
    """
    菜单管理 简单序过滤器
    """

    class Meta:
        model = Menu
        exclude = ('description', 'creator', 'modifier')


class DeptFilter(django_filters.rest_framework.FilterSet):
    """
    部门管理 简单序过滤器
    """

    class Meta:
        model = Dept
        exclude = ('description', 'creator', 'modifier')


class PostFilter(django_filters.rest_framework.FilterSet):
    """
    岗位管理 简单序过滤器
    """

    class Meta:
        model = Post
        exclude = ('description', 'creator', 'modifier')


class RoleFilter(django_filters.rest_framework.FilterSet):
    """
    角色管理 简单序过滤器
    """

    class Meta:
        model = Role
        exclude = ('description', 'creator', 'modifier')


class UserProfileFilter(django_filters.rest_framework.FilterSet):
    """
    用户管理 简单序过滤器
    """
    deptId = django_filters.CharFilter(field_name='dept__id')
    class Meta:
        model = UserProfile
        exclude = ('secret', 'password',)
