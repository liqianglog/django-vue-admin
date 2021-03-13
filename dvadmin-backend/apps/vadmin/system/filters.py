import django_filters

from ..system.models import DictDetails, DictData, ConfigSettings, MessagePush, SaveFile


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


class ConfigSettingsFilter(django_filters.rest_framework.FilterSet):
    """
    参数设置 简单过滤器
    """

    class Meta:
        model = ConfigSettings
        fields = '__all__'


class SaveFileFilter(django_filters.rest_framework.FilterSet):
    """
    文件管理 简单过滤器
    """

    class Meta:
        model = SaveFile
        exclude = ('file',)


class MessagePushFilter(django_filters.rest_framework.FilterSet):
    """
    消息通知 简单过滤器
    """
    # is_read = django_filters.CharFilter(field_name='messagepushuser_message_push__is_read')
    class Meta:
        model = MessagePush
        fields = '__all__'
