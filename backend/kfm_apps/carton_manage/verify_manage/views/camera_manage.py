from _pydecimal import Decimal

import django_filters
from django.db.models import Sum, IntegerField, Q
from django.db.models.functions import Coalesce
from django_filters.rest_framework import FilterSet
from rest_framework import serializers

from carton_manage.verify_manage.models import CameraManage, BackHaulFile
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class CameraManageSerializer(CustomModelSerializer):
    """
   相机管理-序列化器
    """
    device_name = serializers.CharField(source='device.name', read_only=True)
    prod_line_name = serializers.CharField(source='device.production_line.name', read_only=True)
    factory_name = serializers.CharField(source='device.production_line.belong_to_factory.name', read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        _BackHaulFile = BackHaulFile.objects.filter(cam=instance.id).aggregate(
            need_number=Coalesce(Sum('total_number'), 0, output_field=IntegerField()),
            success_number=Coalesce(Sum('success_number'), 0, output_field=IntegerField()),
            error_number=Coalesce(Sum('error_number'), 0, output_field=IntegerField()),
            unrecognized_num=Coalesce(Sum('unrecognized_num'), 0, output_field=IntegerField()),
            code_not_exist_num=Coalesce(Sum('code_not_exist_num'), 0, output_field=IntegerField()),
            self_repetition_num=Coalesce(Sum('self_repetition_num'), 0, output_field=IntegerField()),
            prod_repetition_num=Coalesce(Sum('prod_repetition_num'), 0, output_field=IntegerField()),
            prod_wrong_num=Coalesce(Sum('prod_wrong_num'), 0, output_field=IntegerField()),
        )
        data = {**data, **_BackHaulFile}
        total_number = data['need_number']
        if total_number == 0:
            data['success_rate'] = '0'
        else:
            rate = data['success_number'] / total_number * 100
            data['success_rate'] = str(Decimal(rate).quantize(Decimal('0.00')))
        return data

    class Meta:
        model = CameraManage
        fields = "__all__"
        read_only_fields = ["id"]


class CameraManageCreateUpdateSerializer(CustomModelSerializer):
    """
   相机管理管理 创建/更新时的列化器
    """

    class Meta:
        model = CameraManage
        fields = '__all__'


class CameraManageFilterSet(FilterSet):
    factory_name = django_filters.CharFilter(field_name="device__production_line__belong_to_factory__name",
                                             lookup_expr="icontains")
    prod_line_name = django_filters.CharFilter(field_name="device__production_line__name", lookup_expr="icontains")
    device_name = django_filters.CharFilter(field_name="device__name", lookup_expr="icontains")

    class Meta:
        model = CameraManage
        fields = '__all__'


class CameraManageViewSet(CustomModelViewSet):
    """
   相机管理管理接口:
    """
    queryset = CameraManage.objects.all()
    serializer_class = CameraManageSerializer
    create_serializer_class = CameraManageCreateUpdateSerializer
    update_serializer_class = CameraManageCreateUpdateSerializer
    filter_class = CameraManageFilterSet
    search_fields = ['no']
