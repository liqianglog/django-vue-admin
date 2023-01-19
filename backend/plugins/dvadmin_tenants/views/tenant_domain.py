from django.db import connection

from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin_tenants.models import Domain


class DomainSerializer(CustomModelSerializer):
    """
    租户domain-序列化器
    """

    class Meta:
        model = Domain
        fields = "__all__"
        read_only_fields = ["id"]


class DomainCreateUpdateSerializer(CustomModelSerializer):
    """
    租户domain管理 创建/更新时的列化器
    """

    class Meta:
        model = Domain
        fields = '__all__'


class DomainViewSet(CustomModelViewSet):
    """
    租户domain管理接口:
    """
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    filter_fields = ['domain', 'tenant']

    def get_queryset(self):
        queryset = super().get_queryset()
        if connection.tenant.schema_name != 'public':
            queryset = queryset.filter(tenant__schema_name=connection.tenant.schema_name)
        return queryset

