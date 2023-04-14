# -*- coding: utf-8 -*-
import django_filters
from rest_framework.decorators import action

from basics_manage.models import CustomerInfo
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class CustomerInfoSerializer(CustomModelSerializer):
    """
    客户信息-序列化器
    """

    class Meta:
        model = CustomerInfo
        fields = "__all__"
        read_only_fields = ["id"]


class CustomerInfoCreateUpdateSerializer(CustomModelSerializer):
    """
    客户信息管理 创建/更新时的列化器
    """

    class Meta:
        model = CustomerInfo
        fields = '__all__'

class CustomerInfoFilter(django_filters.FilterSet):
    id = django_filters.AllValuesMultipleFilter(field_name="id",lookup_expr='in')
    class Meta:
        model = CustomerInfo
        fields = "__all__"
        exclude =['attribute_fields']

class CustomerInfoViewSet(CustomModelViewSet):
    """
    客户信息管理接口:
    """
    queryset = CustomerInfo.objects.all()
    serializer_class = CustomerInfoSerializer
    create_serializer_class = CustomerInfoCreateUpdateSerializer
    update_serializer_class = CustomerInfoCreateUpdateSerializer
    filter_class= CustomerInfoFilter
    search_fields = ['no', 'name', 'contacts', 'telephone']

    @action(methods=['get'],detail=True)
    def get_attr_json(self,request,pk):
        """
        获取属性列表
        """
        queyset = CustomerInfo.objects.filter(id=pk).first()
        if queyset:
            data = {
               "attribute_fields": queyset.attribute_fields
            }
            return DetailResponse(data=data)
        else:
            return ErrorResponse(msg="获取失败")
