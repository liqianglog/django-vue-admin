# -*- coding: utf-8 -*-

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
    camera_no = serializers.CharField(source='verify_work_order.cam.no', read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        _BackHaulFile = BackHaulFile.objects.filter(verify_work_order_id=instance.id).aggregate(
            total_num=Coalesce(Sum('total_number'), 0, output_field=IntegerField()),
            success_num=Coalesce(Sum('success_number'), 0, output_field=IntegerField()),
            error_num=Coalesce(Sum('error_number'), 0, output_field=IntegerField()),
            undfind_num = Coalesce(Sum('error_number',filter=Q(verify_code_bhfile__error_type__in=[0])), 0, output_field=IntegerField()),
            inexistence_num = Coalesce(Sum('error_number', filter=Q(verify_code_bhfile__error_type__in=[2])), 0,
                               output_field=IntegerField()),
            self_repetition_num=Coalesce(Sum('error_number', filter=Q(verify_code_bhfile__error_type__in=[3])), 0,
                                     output_field=IntegerField()),
            prod_repetition_num=Coalesce(Sum('error_number', filter=Q(verify_code_bhfile__error_type__in=[4])), 0,
                                         output_field=IntegerField()),
            prod_undfind_num=Coalesce(Sum('error_number', filter=Q(verify_code_bhfile__error_type__in=[5])), 0,
                                         output_field=IntegerField()),
        )
        if _BackHaulFile:
            data['need_number'] = _BackHaulFile.get('total_num')
            data['success_number'] = _BackHaulFile.get('success_num')
            data['error_number'] = _BackHaulFile.get('error_num')
            data['undfind_number'] = _BackHaulFile.get('undfind_num')
            data['inexistence_number'] = _BackHaulFile.get('inexistence_num')
            data['self_repetition_number'] = _BackHaulFile.get('self_repetition_num')
            data['prod_repetition_number'] = _BackHaulFile.get('prod_repetition_num')
            data['prod_undfind_number'] = _BackHaulFile.get('prod_undfind_num')
        else:
            data['need_number'] = 0
            data['success_number'] = 0
            data['error_number'] = 0
            data['undfind_number'] = 0
            data['inexistence_number'] = 0
            data['self_repetition_number'] = 0
            data['prod_repetition_number'] = 0
            data['prod_undfind_number'] = 0
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
    camera_no = django_filters.CharFilter(field_name='verify_work_order__cam__no', lookup_expr="icontains")

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
