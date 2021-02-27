from rest_framework.request import Request

from apps.op_drf.viewsets import CustomModelViewSet
from apps.system.filters import DictDetailsFilter, DictDataFilter, ConfigSettingsFilter
from apps.system.models import DictData, DictDetails, ConfigSettings
from apps.system.serializers import DictDataSerializer, DictDataCreateUpdateSerializer, DictDetailsSerializer, \
    DictDetailsCreateUpdateSerializer, DictDetailsListSerializer, ConfigSettingsSerializer, \
    ConfigSettingsCreateUpdateSerializer
from utils.response import SuccessResponse


class DictDataModelViewSet(CustomModelViewSet):
    """
    字典管理模型的CRUD视图
    """
    queryset = DictData.objects.all()
    serializer_class = DictDataSerializer
    create_serializer_class = DictDataCreateUpdateSerializer
    update_serializer_class = DictDataCreateUpdateSerializer
    # list_serializer_class = ListRoleSerializer
    # retrieve_serializer_class = DetailRoleSerializer
    filter_class = DictDataFilter
    # update_extra_permission_classes = (IsManagerPermission,)
    # destroy_extra_permission_classes = (IsManagerPermission,)
    # create_extra_permission_classes = (IsManagerPermission,)
    search_fields = ('dictName',)
    ordering = 'id'  # 默认排序


class DictDetailsModelViewSet(CustomModelViewSet):
    """
    字典详情 模型的CRUD视图
    """
    queryset = DictDetails.objects.all()
    serializer_class = DictDetailsSerializer
    create_serializer_class = DictDetailsCreateUpdateSerializer
    update_serializer_class = DictDetailsCreateUpdateSerializer
    filter_class = DictDetailsFilter
    # update_extra_permission_classes = (IsManagerPermission,)
    # destroy_extra_permission_classes = (IsManagerPermission,)
    # create_extra_permission_classes = (IsManagerPermission,)
    search_fields = ('dictLabel',)
    ordering = 'sort'  # 默认排序


class DictDetailsListModelViewSet(CustomModelViewSet):
    """
    根据字典类型查询字典数据信息 模型的CRUD视图
    """
    queryset = DictDetails.objects.filter(status=0)
    serializer_class = DictDetailsListSerializer
    filter_class = DictDetailsFilter
    search_fields = ('dictLabel',)
    ordering = 'sort'  # 默认排序

    def list(self, request: Request, *args, **kwargs):
        queryset = self.queryset.filter(dict_data__dictType=kwargs.get('pk')).order_by('sort')
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, *args, **kwargs)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(serializer.data)


class ConfigSettingsModelViewSet(CustomModelViewSet):
    """
    参数设置 模型的CRUD视图
    """
    queryset = ConfigSettings.objects.all()
    serializer_class = ConfigSettingsSerializer
    create_serializer_class = ConfigSettingsCreateUpdateSerializer
    update_serializer_class = ConfigSettingsCreateUpdateSerializer
    filter_class = ConfigSettingsFilter
    # update_extra_permission_classes = (IsManagerPermission,)
    # destroy_extra_permission_classes = (IsManagerPermission,)
    # create_extra_permission_classes = (IsManagerPermission,)
    search_fields = ('name',)
    ordering = 'id'  # 默认排序
