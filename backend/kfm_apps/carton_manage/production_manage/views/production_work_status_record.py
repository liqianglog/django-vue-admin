# -*- coding: utf-8 -*-
import django_filters
from django_filters.rest_framework import FilterSet
from rest_framework import serializers

from carton_manage.production_manage.models import ProductionWorkStatusRecord
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class ProductionWorkStatusRecordSerializer(CustomModelSerializer):
    """
    生产状态记录-序列化器
    """
    production_work_no = serializers.CharField(source="production_work.no",read_only=True)
    code_type = serializers.IntegerField(source="production_work.code_package.code_type",read_only=True)
    order_id = serializers.CharField(source="production_work.order_id", read_only=True)
    factory_info_name = serializers.CharField(source="production_work.factory_info.name", read_only=True)
    production_line_name = serializers.CharField(source="production_work.production_line.name", read_only=True)
    device_name = serializers.CharField(source="production_work.device.name", read_only=True)

    class Meta:
        model = ProductionWorkStatusRecord
        fields = "__all__"
        read_only_fields = ["id"]


class ProductionWorkStatusRecordCreateSerializer(CustomModelSerializer):
    """
    生产状态记录-新增序列化器
    """

    class Meta:
        model = ProductionWorkStatusRecord
        fields = "__all__"
        read_only_fields = ["id"]


class ProductionWorkStatusRecordUpdateSerializer(CustomModelSerializer):
    """
    生产状态记录-更新列化器
    """

    class Meta:
        model = ProductionWorkStatusRecord
        fields = '__all__'


class ProductionWorkStatusRecordFilterSet(FilterSet):
    production_work = django_filters.CharFilter(field_name="production_work__id", lookup_expr="icontains")
    code_type = django_filters.NumberFilter(field_name="production_work__code_package__code_type", lookup_expr="icontains")
    factory_info_name = django_filters.CharFilter(field_name="production_work__factory_info__name", lookup_expr="icontains")
    production_line_name = django_filters.CharFilter(field_name="production_work__production_line__name", lookup_expr="icontains")
    device_name = django_filters.CharFilter(field_name="production_work__device__name", lookup_expr="icontains")


class Meta:
        model = ProductionWorkStatusRecord
        fields = '__all__'

class ProductionWorkStatusRecordViewSet(CustomModelViewSet):
    """
    生产状态记录接口:
    """
    queryset = ProductionWorkStatusRecord.objects.all().order_by('-record_datetime')
    serializer_class = ProductionWorkStatusRecordSerializer
    create_serializer_class = ProductionWorkStatusRecordCreateSerializer
    update_serializer_class = ProductionWorkStatusRecordUpdateSerializer
    filter_class = ProductionWorkStatusRecordFilterSet
