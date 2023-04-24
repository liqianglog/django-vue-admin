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
from carton_manage.production_manage.models import ProductionWork, ProductionWorkVerifyRecord
from dvadmin_tenants.models import Client, Domain


class ProductionWorkSerializer(CustomModelSerializer):
    """
    生产工单管理-序列化器
    """
    factory_info_name = serializers.CharField(source="factory_info.name", read_only=True)
    production_line_name = serializers.CharField(source="production_line.name", read_only=True)
    device_name = serializers.CharField(source="device.name", read_only=True)
    total_number = serializers.IntegerField(source='code_package.total_number', read_only=True)
    product_name = serializers.CharField(source='code_package.product_name', read_only=True)
    arrival_factory = serializers.CharField(source='code_package.arrival_factory', read_only=True)
    code_package_no = serializers.CharField(source="code_package.zip_name", read_only=True, help_text="码包名称")
    order_id = serializers.CharField(source="code_package.order_id", read_only=True, help_text="码包订单ID")
    jet_print_template_name = serializers.CharField(source="jet_print_template.no", read_only=True,
                                                  help_text="喷码模板编号")

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

    @action(methods=['get'], detail=True)
    def production_report(self, request, pk):
        """生产报告"""
        _ProductionWork = ProductionWork.objects.filter(id=pk).first()
        if _ProductionWork is None:
            return ErrorResponse(msg="未查询到生产工单")
        data = {
            "no": _ProductionWork.no,
            "code_package": _ProductionWork.code_package.no,
            "product_name": _ProductionWork.code_package.product_info.name,
            "arrival_factory": _ProductionWork.code_package.arrival_factory,
            "order_id": _ProductionWork.code_package.order_id,
            "status": _ProductionWork.status,
            "device_no": _ProductionWork.device.no,
            "production_line_name": _ProductionWork.production_line.name,
            "factory_info_name": _ProductionWork.factory_info.name,
            "create_datetime": _ProductionWork.create_datetime.strftime("%Y-%m-%d %H:%M:%S" ),
            "update_datetime": _ProductionWork.update_datetime.strftime("%Y-%m-%d %H:%M:%S" ),
            "code_verify_record": ProductionWorkVerifyRecord.objects.filter(production_work_id=pk).values('code_list',
                                                                                                          'result',
                                                                                                          'record_datetime')
        }
        return DetailResponse(data=data)
