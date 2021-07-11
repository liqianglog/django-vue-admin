from apps.vadmin.monitor.models import Server, Monitor
from apps.vadmin.op_drf.serializers import CustomModelSerializer


# ================================================= #
# ************** 服务器信息 序列化器  ************** #
# ================================================= #

class ServerSerializer(CustomModelSerializer):
    """
    服务器信息 简单序列化器
    """

    class Meta:
        model = Server
        fields = ("id", "ip", "name", "os", "remark")


class UpdateServerSerializer(CustomModelSerializer):
    """
    服务器信息 简单序列化器
    """

    class Meta:
        model = Server
        fields = ("name", "remark")


# ================================================= #
# ************** 服务器监控信息 序列化器  ************** #
# ================================================= #

class MonitorSerializer(CustomModelSerializer):
    """
    服务器监控信息 简单序列化器
    """

    class Meta:
        model = Monitor
        fields = '__all__'
