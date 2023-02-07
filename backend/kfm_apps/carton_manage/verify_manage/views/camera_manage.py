from rest_framework import serializers

from carton_manage.verify_manage.models import CameraManage
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class CameraManageSerializer(CustomModelSerializer):
    """
   相机管理-序列化器
    """
    device_name = serializers.CharField(source='device.name',read_only=True)
    prod_line_name = serializers.CharField(source='device.production_line.name', read_only=True)
    factory_name = serializers.CharField(source='device.production_line.belong_to_factory.name', read_only=True)
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
