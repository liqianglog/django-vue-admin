import django_filters

from .models import Project


class ProjectFilter(django_filters.rest_framework.FilterSet):
    """
    项目管理 简单序过滤器
    """
    # 通过 lookup_expr 可进行模糊查询，其他配置可自行百度
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Project
        exclude = ('description', 'creator', 'modifier')
