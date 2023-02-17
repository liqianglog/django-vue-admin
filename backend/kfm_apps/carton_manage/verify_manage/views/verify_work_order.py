# -*- coding: utf-8 -*-
from decimal import Decimal

import django_filters
from django.db.models import Sum, IntegerField, Q
from django.db.models.functions import Coalesce
from django_filters.rest_framework import FilterSet
from rest_framework import serializers
from carton_manage.verify_manage.models import BackHaulFile, VerifyWorkOrder
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class VerifyWorkOrderSerializer(CustomModelSerializer):
    """
    检测工单管理-序列化器
    """
    factory_info_name = serializers.CharField(source="factory_info.name", read_only=True)
    production_line_name = serializers.CharField(source="production_line.name", read_only=True)
    device_name = serializers.CharField(source="device.name", read_only=True)
    total_number = serializers.IntegerField(source='production_work_no.code_package.total_number', read_only=True)
    code_type = serializers.IntegerField(source='production_work_no.code_package.code_type', read_only=True)
    product_name = serializers.CharField(source='production_work_no.code_package.product_name', read_only=True)
    arrival_factory = serializers.CharField(source='production_work_no.code_package.arrival_factory', read_only=True)
    code_package_no = serializers.CharField(source='production_work_no.code_package.no', read_only=True)
    production_work_no = serializers.CharField(source='production_work_no.no', read_only=True)

    def to_representation(self, instance: VerifyWorkOrder):
        data = super().to_representation(instance)
        _BackHaulFile = BackHaulFile.objects.filter(verify_work_order_id=instance.id).aggregate(
            total_num=Coalesce(Sum('total_number'), 0, output_field=IntegerField()),
            success_num=Coalesce(Sum('success_number'), 0, output_field=IntegerField()),
            error_num=Coalesce(Sum('error_number'), 0, output_field=IntegerField()),
            unrecognized_num=Coalesce(Sum('unrecognized_num'), 0, output_field=IntegerField()),
            code_not_exist_num=Coalesce(Sum('code_not_exist_num'), 0, output_field=IntegerField()),
            self_repetition_num=Coalesce(Sum('self_repetition_num'), 0, output_field=IntegerField()),
            prod_repetition_num=Coalesce(Sum('prod_repetition_num'), 0, output_field=IntegerField()),
            prod_wrong_num=Coalesce(Sum('prod_wrong_num'), 0, output_field=IntegerField()),
        )
        total_number = data['need_number']
        success_number = data['success_number']
        if total_number == 0:
            data['success_rate'] = 0
        else:
            rate = success_number / total_number * 100
            data['success_rate'] = str(Decimal(rate).quantize(Decimal('0.00')))
        return data

    class Meta:
        model = VerifyWorkOrder
        fields = "__all__"
        read_only_fields = ["id"]


class VerifyWorkOrderCreateSerializer(CustomModelSerializer):
    """
    检测工单管理-新增序列化器
    """

    class Meta:
        model = VerifyWorkOrder
        fields = "__all__"
        read_only_fields = ["id"]


class VerifyWorkOrderUpdateSerializer(CustomModelSerializer):
    """
    检测工单管理-更新列化器
    """

    class Meta:
        model = VerifyWorkOrder
        fields = '__all__'


class VerifyWorkOrderFilterSet(FilterSet):
    factory_info_name = django_filters.CharFilter(field_name="factory_info__name", lookup_expr="icontains")
    production_line_name = django_filters.CharFilter(field_name="production_line__name", lookup_expr="icontains")
    device_name = django_filters.CharFilter(field_name="device__name", lookup_expr="icontains")

    class Meta:
        model = VerifyWorkOrder
        fields = '__all__'


class VerifyWorkOrderViewSet(CustomModelViewSet):
    """
    检测工单管理接口:
    """
    queryset = VerifyWorkOrder.objects.all()
    serializer_class = VerifyWorkOrderSerializer
    filter_class = VerifyWorkOrderFilterSet
