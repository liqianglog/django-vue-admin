from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from device.models import Terminal


class TerminalSerializer(CustomModelSerializer):
    """终端设备管理序列化器"""

    class Meta:
        model = Terminal
        fields = '__all__'
        read_only_fields = ['id']


class TerminalViewSet(CustomModelViewSet):
    """终端设备管理视图集"""
    queryset = Terminal.objects.all()
    serializer_class = TerminalSerializer
