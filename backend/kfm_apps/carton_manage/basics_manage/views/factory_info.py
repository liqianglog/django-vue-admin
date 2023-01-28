from carton_manage.basics_manage.models import FactoryInfo
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class FactoryInfoSerializer(CustomModelSerializer):
    """
    工厂信息-序列化器
    """

    class Meta:
        model = FactoryInfo
        fields = "__all__"
        read_only_fields = ["id"]


class FactoryInfoCreateUpdateSerializer(CustomModelSerializer):
    """
    工厂信息管理 创建/更新时的列化器
    """

    class Meta:
        model = FactoryInfo
        fields = '__all__'


class FactoryInfoViewSet(CustomModelViewSet):
    """
    工厂信息管理接口:
    """
    queryset = FactoryInfo.objects.all()
    serializer_class = FactoryInfoSerializer
    create_serializer_class = FactoryInfoCreateUpdateSerializer
    update_serializer_class = FactoryInfoCreateUpdateSerializer
    search_fields = ['code', 'name', 'contacts', 'telephone']
