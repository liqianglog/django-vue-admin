# -*- coding: utf-8 -*-
import django_filters

from basics_manage.models import ProductInfo
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class ProductInfoSerializer(CustomModelSerializer):
    """
    产品信息-序列化器
    """

    class Meta:
        model = ProductInfo
        fields = "__all__"
        read_only_fields = ["id"]


class ProductInfoCreateUpdateSerializer(CustomModelSerializer):
    """
    产品信息管理 创建/更新时的列化器
    """

    class Meta:
        model = ProductInfo
        fields = '__all__'

class ProductInfoFilter(django_filters.FilterSet):
    id = django_filters.AllValuesMultipleFilter(field_name="id",lookup_expr='in')
    class Meta:
        model = ProductInfo
        fields = "__all__"

class ProductInfoViewSet(CustomModelViewSet):
    """
    产品信息管理接口:
    """
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer
    create_serializer_class = ProductInfoCreateUpdateSerializer
    update_serializer_class = ProductInfoCreateUpdateSerializer
    filter_class = ProductInfoFilter
    search_fields = ['no', 'name', 'contacts', 'telephone']
