from django.db.models import Q
from rest_framework.request import Request

from ..op_drf.filters import DataLevelPermissionsFilter
from ..op_drf.viewsets import CustomModelViewSet
from ..system.filters import DictDetailsFilter, DictDataFilter, ConfigSettingsFilter, MessagePushFilter, \
    SaveFileFilter
from ..system.models import DictData, DictDetails, ConfigSettings, SaveFile, MessagePush
from ..system.models import MessagePushUser
from ..system.serializers import DictDataSerializer, DictDataCreateUpdateSerializer, DictDetailsSerializer, \
    DictDetailsCreateUpdateSerializer, DictDetailsListSerializer, ConfigSettingsSerializer, \
    ConfigSettingsCreateUpdateSerializer, SaveFileSerializer, SaveFileCreateUpdateSerializer, \
    ExportConfigSettingsSerializer, ExportDictDataSerializer, ExportDictDetailsSerializer, \
    MessagePushSerializer, MessagePushCreateUpdateSerializer, ExportMessagePushSerializer
from ..utils.export_excel import export_excel_save_model
from ..utils.response import SuccessResponse


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

    def export(self, request: Request, *args, **kwargs):
        """
        导出字典管理数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        field_data = ['字典主键', '字典名称', '字典类型', '字典状态', '创建者', '修改者', '备注']
        data = ExportDictDataSerializer(DictData.objects.all(), many=True).data
        return SuccessResponse(export_excel_save_model(request, field_data, data, '导出参数管理数据.xls'))


class DictDetailsModelViewSet(CustomModelViewSet):
    """
    字典详情 模型的CRUD视图
    """
    queryset = DictDetails.objects.all()
    serializer_class = DictDetailsSerializer
    create_serializer_class = DictDetailsCreateUpdateSerializer
    update_serializer_class = DictDetailsCreateUpdateSerializer
    filter_class = DictDetailsFilter
    extra_filter_backends = [DataLevelPermissionsFilter]
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

    def export(self, request: Request, *args, **kwargs):
        """
        导出字典详情数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        dictType = request.query_params.get('dictType')
        field_data = ['字典详情主键', '字典标签', '字典键值', '是否默认', '字典状态', '字典排序', '创建者', '修改者', '备注']
        data = ExportDictDetailsSerializer(DictDetails.objects.filter(dict_data__dictType=dictType), many=True).data
        return SuccessResponse(export_excel_save_model(request, field_data, data, f'导出字典[{dictType}]详情数据.xls'))


class ConfigSettingsModelViewSet(CustomModelViewSet):
    """
    参数设置 模型的CRUD视图
    """
    queryset = ConfigSettings.objects.all()
    serializer_class = ConfigSettingsSerializer
    create_serializer_class = ConfigSettingsCreateUpdateSerializer
    update_serializer_class = ConfigSettingsCreateUpdateSerializer
    filter_class = ConfigSettingsFilter
    extra_filter_backends = [DataLevelPermissionsFilter]
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

    def export(self, request: Request, *args, **kwargs):
        """
        导出参数管理数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        field_data = ['参数主键', '参数名称', '参数键名', '参数键值', '系统内置', '参数状态', '创建者', '修改者', '备注']
        data = ExportConfigSettingsSerializer(ConfigSettings.objects.all(), many=True).data
        return SuccessResponse(export_excel_save_model(request, field_data, data, '导出参数管理数据.xls'))


class SaveFileModelViewSet(CustomModelViewSet):
    """
   文件管理 模型的CRUD视图
   """
    queryset = SaveFile.objects.all()
    serializer_class = SaveFileSerializer
    create_serializer_class = SaveFileCreateUpdateSerializer
    update_serializer_class = SaveFileCreateUpdateSerializer
    filter_class = SaveFileFilter
    extra_filter_backends = [DataLevelPermissionsFilter]
    search_fields = ('configName',)
    ordering = 'id'  # 默认排序


class MessagePushModelViewSet(CustomModelViewSet):
    """
    消息推送模型的CRUD视图
    """
    queryset = MessagePush.objects.all()
    serializer_class = MessagePushSerializer
    create_serializer_class = MessagePushCreateUpdateSerializer
    update_serializer_class = MessagePushCreateUpdateSerializer
    extra_filter_backends = [DataLevelPermissionsFilter]
    filter_class = MessagePushFilter
    ordering = "-update_datetime"  # 默认排序

    def get_message_list(self, request: Request, *args, **kwargs):
        """
            管理员获取自己的消息列表
        """
        messages = self.queryset.filter(**kwargs)
        data = MessagePushSerializer(messages, many=True)
        return SuccessResponse(msg="返回", data=data)

    def get_user_messages(self, request: Request, *args, **kwargs):
        """
        获取用户自己消息列表
        """
        queryset = self.filter_queryset(self.get_queryset())
        is_read = request.query_params.get('is_read', None)
        if is_read:
            if is_read == 'False':
                queryset = queryset.filter(Q(messagepushuser_message_push__is_read=is_read) | Q(user=None))
            else:
                queryset = queryset.filter(messagepushuser_message_push__is_read=is_read)

        queryset = queryset.filter(is_reviewed=True)
        page = self.paginate_queryset(queryset)
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, *args, **kwargs)
        if page is not None:
            if getattr(self, 'values_queryset', None):
                return self.get_paginated_response(page)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        if getattr(self, 'values_queryset', None):
            return SuccessResponse(page)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(serializer.data)

    def update_is_read(self, request: Request, *args, **kwargs):
        """
        修改为已读
        """
        instance, _ = MessagePushUser.objects.get_or_create(message_push_id=kwargs.get('pk'), user=request.user)
        instance.is_read = True
        instance.save()
        return SuccessResponse()

    def export(self, request: Request, *args, **kwargs):
        """
        导出岗位
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        field_data = ['消息序号', '标题', '内容', '消息类型', '是否审核', '消息状态', '通知接收消息用户', '创建者', '修改者', '修改时间', '创建时间']
        data = ExportMessagePushSerializer(MessagePush.objects.all(), many=True).data
        return SuccessResponse(export_excel_save_model(request, field_data, data, '导出岗位数据.xls'))
