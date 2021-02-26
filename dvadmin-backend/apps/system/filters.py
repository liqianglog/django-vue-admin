import django_filters

from apps.system.models import DictDetails, DictData


class DictDataFilter(django_filters.rest_framework.FilterSet):
    """
    字典管理 简单过滤器
    """
    class Meta:
        model = DictData
        fields = '__all__'


class DictDetailsFilter(django_filters.rest_framework.FilterSet):
    """
    字典详情 简单过滤器
    """
    dictType = django_filters.CharFilter(field_name='dict_data__dictType')
    class Meta:
        model = DictDetails
        fields = '__all__'
