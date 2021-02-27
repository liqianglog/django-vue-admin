import os

from django.conf import settings
from django.http import HttpResponse
from rest_framework.request import Request

from apps.op_drf.viewsets import CustomModelViewSet
from apps.system.filters import DictDetailsFilter, DictDataFilter, ConfigSettingsFilter
from apps.system.models import DictData, DictDetails, ConfigSettings, SaveFile
from apps.system.serializers import DictDataSerializer, DictDataCreateUpdateSerializer, DictDetailsSerializer, \
    DictDetailsCreateUpdateSerializer, DictDetailsListSerializer, ConfigSettingsSerializer, \
    ConfigSettingsCreateUpdateSerializer, SaveFileSerializer, SaveFileCreateUpdateSerializer
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

    def dict_details_list(self, request: Request, *args, **kwargs):
        """
        根据字典类型查询字典数据信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        queryset = self.queryset.filter(dict_data__dictType=kwargs.get('pk')).order_by('sort')
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, *args, **kwargs)
        serializer = DictDetailsListSerializer(queryset, many=True)
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
    search_fields = ('configName',)
    ordering = 'id'  # 默认排序

    def get_config_key(self, request: Request, *args, **kwargs):
        """
        根据 参数键名 查询参数数据信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        queryset = self.queryset.filter(configKey=kwargs.get('pk')).first()
        # if hasattr(self, 'handle_logging'):
        #     self.handle_logging(request, *args, **kwargs)
        return SuccessResponse(msg=queryset.configValue if queryset else '')


class SaveFileModelViewSet(CustomModelViewSet):
    """
   参数设置 模型的CRUD视图
   """
    queryset = SaveFile.objects.all()
    serializer_class = SaveFileSerializer
    create_serializer_class = SaveFileCreateUpdateSerializer
    update_serializer_class = SaveFileCreateUpdateSerializer
    # filter_class = ConfigSettingsFilter
    search_fields = ('configName',)
    ordering = 'id'  # 默认排序

    def download_file(self, request: Request, *args, **kwargs):
        """
        下载文件
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        file_path = os.path.join(settings.MEDIA_ROOT,str(instance.file))
        with open(file_path, "rb") as f:
            res = HttpResponse(f)
        res["Content-Type"] = instance.type  # 注意格式
        res["Content-Disposition"] = 'filename="{}"'.format(instance.name)
        return res
