from .filters import ServerFilter, MonitorFilter
from .models import Server, Monitor
from .serializers import ServerSerializer, MonitorSerializer
from ..op_drf.viewsets import CustomModelViewSet
from ..permission.permissions import CommonPermission


class ServerModelViewSet(CustomModelViewSet):
    """
    服务器信息 模型的CRUD视图
    """
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    # extra_filter_backends = [DataLevelPermissionsFilter]
    filter_class = ServerFilter
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    ordering = '-create_datetime'  # 默认排序

class MonitorModelViewSet(CustomModelViewSet):
    """
    服务器监控信息 模型的CRUD视图
    """
    queryset = Monitor.objects.all()
    serializer_class = MonitorSerializer
    # extra_filter_backends = [DataLevelPermissionsFilter]
    filter_class = MonitorFilter
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    ordering = '-create_datetime'  # 默认排序
