from rest_framework import serializers

from carton_manage.verify_manage.models import BackHaulFile
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class BackHaulFileSerializer(CustomModelSerializer):
    """
   回传文件管理-序列化器
    """
    device_name = serializers.CharField(source='device.name',read_only=True)
    prod_line_name = serializers.CharField(source='device.production_line.name', read_only=True)
    factory_name = serializers.CharField(source='device.production_line.belong_to_factory.name', read_only=True)
    class Meta:
        model = BackHaulFile
        fields = "__all__"
        read_only_fields = ["id"]


class BackHaulFileCreateUpdateSerializer(CustomModelSerializer):
    """
   回传文件管理管理 创建/更新时的列化器
    """

    class Meta:
        model = BackHaulFile
        fields = '__all__'


class BackHaulFileViewSet(CustomModelViewSet):
    """
   回传文件管理管理接口:
    """
    queryset = BackHaulFile.objects.all()
    serializer_class = BackHaulFileSerializer
    create_serializer_class = BackHaulFileCreateUpdateSerializer
    update_serializer_class = BackHaulFileCreateUpdateSerializer

