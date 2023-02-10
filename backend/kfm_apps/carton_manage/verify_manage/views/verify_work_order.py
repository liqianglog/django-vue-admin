# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import posixpath
from urllib.parse import urlsplit

import django_filters
from django.core.cache import cache
from django.db import connection
from django.db.models import Sum, IntegerField
from django.db.models.functions import Coalesce
from django_filters.rest_framework import FilterSet
from django_tenants.utils import schema_context
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from application import settings
from basics_manage.models import ProductionLine, DeviceManage
from carton_manage.verify_manage.models import BackHaulFile
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from carton_manage.code_manage.models import CodePackage
from carton_manage.production_manage.models import ProductionWork
from dvadmin_tenants.models import Client, Domain


class VerifyWorkOrderSerializer(CustomModelSerializer):
    """
    生产工单管理-序列化器
    """
    factory_info_name = serializers.CharField(source="factory_info.name", read_only=True)
    production_line_name = serializers.CharField(source="production_line.name", read_only=True)
    device_name= serializers.CharField(source="device.name", read_only=True)
    total_number = serializers.IntegerField(source='code_package.total_number',read_only=True)
    code_type = serializers.IntegerField(source='code_package.code_type',read_only=True)
    product_name = serializers.CharField(source='code_package.product_name',read_only=True)
    arrival_factory = serializers.CharField(source='code_package.arrival_factory',read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        _BackHaulFile = BackHaulFile.objects.filter(production_work=instance.id).annotate(
            total_num=Coalesce(Sum('total_number'), 0, output_field=IntegerField()),
            success_num=Coalesce(Sum('success_number'), 0, output_field=IntegerField()),
            error_num=Coalesce(Sum('error_number'), 0, output_field=IntegerField())
        )
        if _BackHaulFile:
            data['need_number'] = _BackHaulFile.get('total_num')
            data['success_number'] = _BackHaulFile.get('success_num')
            data['error_number'] = _BackHaulFile.get('error_num')
        else:
            data['need_number'] = 0
            data['success_number'] = 0
            data['error_number'] = 0
        return data

    class Meta:
        model = ProductionWork
        fields = "__all__"
        read_only_fields = ["id"]


class VerifyWorkOrderCreateSerializer(CustomModelSerializer):
    """
    生产工单管理-新增序列化器
    """
    class Meta:
        model = ProductionWork
        fields = "__all__"
        read_only_fields = ["id"]


class VerifyWorkOrderUpdateSerializer(CustomModelSerializer):
    """
    生产工单管理-更新列化器
    """

    class Meta:
        model = ProductionWork
        fields = '__all__'

class VerifyWorkOrderFilterSet(FilterSet):
    factory_info_name = django_filters.CharFilter(field_name="factory_info__name", lookup_expr="icontains")
    production_line_name = django_filters.CharFilter(field_name="production_line__name", lookup_expr="icontains")
    device_name = django_filters.CharFilter(field_name="device__name", lookup_expr="icontains")

    class Meta:
        model = ProductionWork
        fields = '__all__'

class VerifyWorkOrderViewSet(CustomModelViewSet):
    """
    生产工单管理接口:
    """
    queryset = ProductionWork.objects.all()
    serializer_class = VerifyWorkOrderSerializer
    filter_class = VerifyWorkOrderFilterSet