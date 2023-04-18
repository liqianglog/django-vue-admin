from django.db import connection
from django_tenants.utils import tenant_context

from application import dispatch
from dvadmin.system.management.commands import init_area
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin_tenants.models import Client, HistoryCodeInfo


class ClientSerializer(CustomModelSerializer):
    """
    租户信息-序列化器
    """

    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ["id"]

    def create(self, validated_data):
        instance = super().create(validated_data)
        # 初始化信息
        with tenant_context(instance):
            from dvadmin_tenants.management.commands.tenant_init import Command
            res = Command()
            res.run()
            print("初始化数据初始完毕")
            # 初始化省份城市
            init_area.main()
            print("省份数据初始化完毕")
            # 初始化ck表
            # =========== 初始化系统配置 =================
            dispatch.init_system_config()
            dispatch.init_dictionary()
            print("租户所有初始化完成!")
            # ==========================================
            HistoryCodeInfo.set_db().create_table()
        return instance


class ClientCreateUpdateSerializer(CustomModelSerializer):
    """
    租户信息管理 创建/更新时的列化器
    """

    class Meta:
        model = Client
        fields = '__all__'


class ClientViewSet(CustomModelViewSet):
    """
    租户信息管理接口:
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_fields = ['name', 'schema_name']

    def get_queryset(self):
        queryset = super().get_queryset()
        if connection.tenant.schema_name != 'public':
            queryset = queryset.filter(schema_name=connection.tenant.schema_name)
        return queryset
