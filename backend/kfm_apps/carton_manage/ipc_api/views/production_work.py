# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import posixpath
from urllib.parse import urlsplit

from django.db import connection
from django_tenants.utils import schema_context
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from application import settings
from basics_manage.models import ProductionLine, DeviceManage
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from carton_manage.code_manage.models import CodePackage
from carton_manage.production_manage.models import ProductionWork
from dvadmin_tenants.models import Client, Domain


class IpcProductionWorkSerializer(CustomModelSerializer):
    """
    生产工单管理-序列化器
    """
    package_template_no = serializers.CharField(source="no", read_only=True)

    class Meta:
        model = ProductionWork
        fields = [
            'package_template_no',
            "char_length",
            "fields",
            "separator",
            "line_feed",
            "code_type",
            "w_url_prefix",
            "w_url_length",
            "w_field_position",
            "n_url_prefix",
            "n_url_length",
            "n_field_position",
        ]
        read_only_fields = ["id"]


class IpcProductionWorkCreateSerializer(CustomModelSerializer):
    """
    生产工单管理-新增序列化器
    """
    def to_representation(self,instance):
        file_position = posixpath.normpath(instance.code_package.file_position).lstrip('/')
        result = {
        "code_pack_id": instance.code_package.id,
        "code_pack_no":instance.code_package.no,
        "code_pack_name": instance.code_package.zip_name,
        "work_no":instance.no,
        "filemd5": instance.code_package.file_md5,
        "first_line_md5": instance.code_package.first_line_md5,
        "total_number": instance.code_package.total_number,
        "keyid": instance.code_package.key_id,
        "file_url": file_position
        }
        if connection.tenant.schema_name == "public":
            schema_name_list = Client.objects.exclude(schema_name="public").values_list('schema_name', flat=True)
        else:
            schema_name_list = [connection.tenant.schema_name]
        _DeviceManage = None
        _schema_name = None
        # 通过设备编号从所有租户中获取设备
        for schema_name in schema_name_list:
            with schema_context(schema_name):
                request = self.request
                device_id = request.user.device_id
                _DeviceManage = DeviceManage.objects.filter(id=device_id).first()
                if _DeviceManage:
                    _schema_name = schema_name
                    domain_obj = Domain.objects.filter(is_primary=True, tenant__schema_name=schema_name).first()
                    http = urlsplit(request.build_absolute_uri(None)).scheme
                    if settings.ENVIRONMENT == "prod":
                        result['file_url'] = f"https://{domain_obj.domain}/api/carton/ipc/download_code_package_file/{_schema_name}/{file_position}"
                    elif settings.ENVIRONMENT == "test":
                        result['file_url'] = f"http://{domain_obj.domain}/api/carton/ipc/download_code_package_file/{_schema_name}/{file_position}"
                    else:
                        result['file_url'] = f"{http}://{domain_obj.domain}:{request.META['SERVER_PORT']}/api/carton/ipc/download_code_package_file/{_schema_name}/{file_position}"
        return result

    class Meta:
        model = ProductionWork
        fields = "__all__"
        read_only_fields = ["id"]


class IpcProductionWorkUpdateSerializer(CustomModelSerializer):
    """
    生产工单管理-更新列化器
    """

    class Meta:
        model = ProductionWork
        fields = '__all__'


class ProductionWorkViewSet(CustomModelViewSet):
    """
    生产工单管理接口:
    """
    queryset = ProductionWork.objects.all()
    serializer_class = IpcProductionWorkSerializer
    create_serializer_class = IpcProductionWorkCreateSerializer
    update_serializer_class = IpcProductionWorkUpdateSerializer

    @action(methods=['post'],detail=False,permission_classes=[IsAuthenticated])
    def bind_code_package(self, request, *args, **kwargs):
        #码包绑定
        data = request.data
        work_no = data.get('work_no',None)
        code_pack_id= data.get('code_pack_id',None)
        if work_no is None:
            return ErrorResponse(msg="未获取到生产工单号")
        if code_pack_id is None:
            return ErrorResponse(msg="未获取到码包号")
        else:
            # print(request.user.device_id)
            # print(request.user.production_line_id)
            code_package_instance = CodePackage.objects.filter(id=code_pack_id).first()
            if code_package_instance is None:
                return ErrorResponse(msg="未查询到码包号")
            else:
                device = request.user.device_id
                production_line = request.user.production_line_id
                production_line_queryset = ProductionLine.objects.filter(id=production_line).first()
                create_data = {
                    "no":work_no,
                    "code_package":code_pack_id,
                    "order_id":code_package_instance.order_id,
                    "device":device,
                    "production_line":production_line,
                    "factory_info":production_line_queryset.belong_to_factory.id
                }
                serializer=IpcProductionWorkCreateSerializer(data=create_data,many=False,request=request)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return DetailResponse(data=serializer.data)

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def before_verify(self,request):
        data = request.data
        work_no = data.get('work_no',None)
        if work_no is None:
            return ErrorResponse(msg="未获取到生产工单号")
        code_type= data.get('code_type',None)
        if code_type is None:
            return ErrorResponse(msg="未获取到码类型")
        code_list= data.get('code_list',None)
        if code_list is None:
            return ErrorResponse(msg="未获取到码内容")
        _ProductionWork = ProductionWork.objects.filter(no=work_no).first()
        if _ProductionWork is None:
            return ErrorResponse(msg="未查询到生产工单号")
        return DetailResponse(msg="码包正常")


    @action(methods=['post'],detail=False,permission_classes=[IsAuthenticated])
    def change(self,request):
        #生产工单变化
        data = request.data
        work_no =data.get('work_no',None)
        print_position = data.get('print_position',None)
        work_status = data.get('work_status',None)
        if work_no is None:
            return ErrorResponse(msg="未获取到生产工单号")
        else:
            production_work_instance = ProductionWork.objects.filter(no=work_no).first()
            if production_work_instance is None:
                return ErrorResponse(msg="未查询到生产工单号")
            else:
                if print_position is None:
                    return ErrorResponse(msg="未获取到打印位置")
                if work_status is None:
                    return ErrorResponse(msg="未获取到生产状态")
                production_work_instance.print_position = print_position
                production_work_instance.status = work_status
                production_work_instance.save()
                return DetailResponse(msg="更新成功")