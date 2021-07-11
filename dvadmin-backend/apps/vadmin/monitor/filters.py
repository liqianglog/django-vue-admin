import django_filters

from apps.vadmin.monitor.models import Server, Monitor


class ServerFilter(django_filters.rest_framework.FilterSet):
    """
    服务器信息 简单过滤器
    """

    class Meta:
        model = Server
        fields = '__all__'


class MonitorFilter(django_filters.rest_framework.FilterSet):
    """
    服务器监控信息 简单过滤器
    """

    class Meta:
        model = Monitor
        fields = '__all__'
