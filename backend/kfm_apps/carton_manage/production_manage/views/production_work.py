# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import posixpath
from urllib.parse import urlsplit

import django_filters
from django.core.cache import cache
from django.db import connection
from django_filters.rest_framework import FilterSet
from django_tenants.utils import schema_context
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from application import settings
from basics_manage.models import ProductionLine, DeviceManage
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from carton_manage.code_manage.models import CodePackage
from carton_manage.production_manage.models import ProductionWork
from dvadmin_tenants.models import Client, Domain


class ProductionWorkSerializer(CustomModelSerializer):
    """
    生产工单管理-序列化器
    """
    factory_info_name = serializers.CharField(source="factory_info.name", read_only=True)
    production_line_name = serializers.CharField(source="production_line.name", read_only=True)
    device_name= serializers.CharField(source="device.name", read_only=True)

    class Meta:
        model = ProductionWork
        fields = "__all__"
        read_only_fields = ["id"]


class ProductionWorkCreateSerializer(CustomModelSerializer):
    """
    生产工单管理-新增序列化器
    """
    class Meta:
        model = ProductionWork
        fields = "__all__"
        read_only_fields = ["id"]


class ProductionWorkUpdateSerializer(CustomModelSerializer):
    """
    生产工单管理-更新列化器
    """

    class Meta:
        model = ProductionWork
        fields = '__all__'

class ProductionWorkFilterSet(FilterSet):
    factory_info_name = django_filters.CharFilter(field_name="factory_info__name", lookup_expr="icontains")
    production_line_name = django_filters.CharFilter(field_name="production_line__name", lookup_expr="icontains")
    device_name = django_filters.CharFilter(field_name="device__name", lookup_expr="icontains")

    class Meta:
        model = ProductionWork
        fields = '__all__'

class ProductionWorkViewSet(CustomModelViewSet):
    """
    生产工单管理接口:
    """
    queryset = ProductionWork.objects.all()
    serializer_class = ProductionWorkSerializer
    create_serializer_class = ProductionWorkCreateSerializer
    update_serializer_class = ProductionWorkUpdateSerializer
    filter_class = ProductionWorkFilterSet