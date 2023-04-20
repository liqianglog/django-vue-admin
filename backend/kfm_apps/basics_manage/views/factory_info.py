import django_filters

from basics_manage.models import FactoryInfo
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


class FactoryInfoFilter(django_filters.FilterSet):
    id = django_filters.AllValuesMultipleFilter(field_name="id",lookup_expr='in')
    class Meta:
        model = FactoryInfo
        fields = "__all__"

class FactoryInfoViewSet(CustomModelViewSet):
    """
    工厂信息管理接口:
    """
    queryset = FactoryInfo.objects.all()
    serializer_class = FactoryInfoSerializer
    create_serializer_class = FactoryInfoCreateUpdateSerializer
    update_serializer_class = FactoryInfoCreateUpdateSerializer
    filter_class = FactoryInfoFilter
    search_fields = ['code', 'name', 'contacts', 'telephone']
