# -*- coding: utf-8 -*-
import json

import django_filters
from django_filters.rest_framework import FilterSet
from rest_framework import serializers

from carton_manage.production_manage.models import ProductionWorkVerifyRecord
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class ProductionWorkVerifyRecordSerializer(CustomModelSerializer):
    """
    生产校验记录-序列化器
    """
    production_work_no = serializers.CharField(source="production_work.no", read_only=True)
    code_type = serializers.IntegerField(source="production_work.code_package.code_type", read_only=True)
    order_id = serializers.CharField(source="production_work.order_id", read_only=True)
    factory_info_name = serializers.CharField(source="production_work.factory_info.name", read_only=True)
    production_line_name = serializers.CharField(source="production_work.production_line.name", read_only=True)
    device_name = serializers.CharField(source="production_work.device.name", read_only=True)

    class Meta:
        model = ProductionWorkVerifyRecord
        fields = "__all__"
        read_only_fields = ["id"]


class ProductionWorkVerifyRecordCreateSerializer(CustomModelSerializer):
    """
    生产校验记录-新增序列化器
    """

    class Meta:
        model = ProductionWorkVerifyRecord
        fields = "__all__"
        read_only_fields = ["id"]


class ProductionWorkVerifyRecordUpdateSerializer(CustomModelSerializer):
    """
    生产校验记录-更新列化器
    """

    class Meta:
        model = ProductionWorkVerifyRecord
        fields = '__all__'


class ProductionWorkVerifyRecordFilterSet(FilterSet):
    factory_info_name = django_filters.CharFilter(field_name="production_work__factory_info__name",
                                                  lookup_expr="icontains")
    production_line_name = django_filters.CharFilter(field_name="production_work__production_line__name",
                                                     lookup_expr="icontains")
    device_name = django_filters.CharFilter(field_name="production_work__device__name", lookup_expr="icontains")


class Meta:
    model = ProductionWorkVerifyRecord
    fields = '__all__'


class ProductionWorkVerifyRecordViewSet(CustomModelViewSet):
    """
    生产校验记录接口:
    """
    queryset = ProductionWorkVerifyRecord.objects.all()
    serializer_class = ProductionWorkVerifyRecordSerializer
    create_serializer_class = ProductionWorkVerifyRecordCreateSerializer
    update_serializer_class = ProductionWorkVerifyRecordUpdateSerializer
    filter_class = ProductionWorkVerifyRecordFilterSet
