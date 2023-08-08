from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from device.models import Gateway


class GatewaySerializer(CustomModelSerializer):
    """网关管理序列化器"""

    class Meta:
        model = Gateway
        fields = '__all__'
        read_only_fields = ['id']


class GatewayViewSet(CustomModelViewSet):
    """网关管理视图集"""
    queryset = Gateway.objects.all()
    serializer_class = GatewaySerializer
