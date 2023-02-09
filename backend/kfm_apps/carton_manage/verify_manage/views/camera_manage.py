from _pydecimal import Decimal

from django.db.models import Sum, IntegerField
from django.db.models.functions import Coalesce
from rest_framework import serializers

from carton_manage.verify_manage.models import CameraManage, BackHaulFile
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class CameraManageSerializer(CustomModelSerializer):
    """
   相机管理-序列化器
    """
    device_name = serializers.CharField(source='device.name',read_only=True)
    prod_line_name = serializers.CharField(source='device.production_line.name', read_only=True)
    factory_name = serializers.CharField(source='device.production_line.belong_to_factory.name', read_only=True)
    # total_number = serializers.SerializerMethodField(help_text='识别码总数')
    # success_number = serializers.SerializerMethodField(help_text='识别成功数')
    # error_number = serializers.SerializerMethodField(help_text='识别失败数')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        device = instance.device.id
        _BackHaulFile = BackHaulFile.objects.filter(device=device).annotate(
            total_num = Coalesce(Sum('total_number'),0,output_field=IntegerField()),
            success_num=Coalesce(Sum('success_number'),0,output_field=IntegerField()),
            error_num=Coalesce(Sum('error_number'),0,output_field=IntegerField())
        )
        if _BackHaulFile:
            data['total_number'] = _BackHaulFile.get('total_num')
            data['success_number'] = _BackHaulFile.get('success_num')
            data['error_number'] = _BackHaulFile.get('error_num')
            if _BackHaulFile.get('total_num')==0:
                data['success_rate'] = 0
            else:
                rate = _BackHaulFile.get('success_num') / _BackHaulFile.get('total_num')
                data['success_rate'] = Decimal(rate).quantize(Decimal('0.00'))
        else:
            data['total_number'] = 0
            data['success_number'] = 0
            data['error_number'] = 0
            data['success_rate'] = 0
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


class CameraManageViewSet(CustomModelViewSet):
    """
   相机管理管理接口:
    """
    queryset = CameraManage.objects.all()
    serializer_class = CameraManageSerializer
    create_serializer_class = CameraManageCreateUpdateSerializer
    update_serializer_class = CameraManageCreateUpdateSerializer
    search_fields = ['no']
