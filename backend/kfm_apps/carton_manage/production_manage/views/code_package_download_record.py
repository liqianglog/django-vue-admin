# -*- coding: utf-8 -*-
import django_filters
from django_filters.rest_framework import FilterSet
from rest_framework import serializers

from carton_manage.production_manage.models import CodePackageDownloadRecord
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class CodePackageDownloadRecordSerializer(CustomModelSerializer):
    """
    生产状态记录-序列化器
    """
    production_work_no = serializers.CharField(source="production_work.no",read_only=True)
    order_id = serializers.CharField(source="production_work.code_package.order_id", read_only=True)
    factory_info_name = serializers.CharField(source="production_work.factory_info.name", read_only=True)
    production_line_name = serializers.CharField(source="production_work.production_line.name", read_only=True)
    device_name = serializers.CharField(source="device.name", read_only=True)

    class Meta:
        model = CodePackageDownloadRecord
        fields = "__all__"
        read_only_fields = ["id"]


class CodePackageDownloadRecordCreateSerializer(CustomModelSerializer):
    """
    生产状态记录-新增序列化器
    """

    class Meta:
        model = CodePackageDownloadRecord
        fields = "__all__"
        read_only_fields = ["id"]


class CodePackageDownloadRecordUpdateSerializer(CustomModelSerializer):
    """
    生产状态记录-更新列化器
    """

    class Meta:
        model = CodePackageDownloadRecord
        fields = '__all__'


class CodePackageDownloadRecordFilterSet(FilterSet):
    factory_info_name = django_filters.CharFilter(field_name="production_work__factory_info__name", lookup_expr="icontains")
    production_line_name = django_filters.CharFilter(field_name="production_work__production_line__name", lookup_expr="icontains")
    device_name = django_filters.CharFilter(field_name="device__name", lookup_expr="icontains")


class Meta:
        model = CodePackageDownloadRecord
        fields = '__all__'

class CodePackageDownloadRecordViewSet(CustomModelViewSet):
    """
    生产状态记录接口:
    """
    queryset = CodePackageDownloadRecord.objects.all().order_by('-record_datetime')
    serializer_class = CodePackageDownloadRecordSerializer
    create_serializer_class = CodePackageDownloadRecordCreateSerializer
    update_serializer_class = CodePackageDownloadRecordUpdateSerializer
    filter_class = CodePackageDownloadRecordFilterSet
