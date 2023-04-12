# -*- coding: utf-8 -*-
from basics_manage.models import CustomerInfo
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


class CustomerInfoViewSet(CustomModelViewSet):
    """
    客户信息管理接口:
    """
    queryset = CustomerInfo.objects.all()
    serializer_class = CustomerInfoSerializer
    create_serializer_class = CustomerInfoCreateUpdateSerializer
    update_serializer_class = CustomerInfoCreateUpdateSerializer
    search_fields = ['no', 'name', 'contacts', 'telephone']
