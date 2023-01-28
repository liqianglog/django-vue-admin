import django_filters
from rest_framework import serializers

from carton_manage.basics_manage.models import ProductionLine
from dvadmin.system.models import Dept
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class ProductionLineSerializer(CustomModelSerializer):
    """
    产线信息-序列化器
    """

    class Meta:
        model = ProductionLine
        fields = "__all__"
        read_only_fields = ["id"]


class ProductionLineCreateUpdateSerializer(CustomModelSerializer):
    """
    产线信息管理 创建/更新时的列化器
    """

    class Meta:
        model = ProductionLine
        fields = '__all__'


class ProductionLineViewSet(CustomModelViewSet):
    """
    产线信息管理接口:
    """
    queryset = ProductionLine.objects.all()
    serializer_class = ProductionLineSerializer
    create_serializer_class = ProductionLineCreateUpdateSerializer
    update_serializer_class = ProductionLineCreateUpdateSerializer
    search_fields = ['code', 'name']
