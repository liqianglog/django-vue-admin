# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from basics_manage.models import ProductionLine
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from carton_manage.code_manage.models import CodePackage
from carton_manage.production_manage.models import ProductionWork


class IpcProductionWorkSerializer(CustomModelSerializer):
    """
    码包模板管理-序列化器
    """
    package_template_no = serializers.CharField(source="no", read_only=True)

    # def to_representation(self,obj):
    #     pass
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
    码包模板管理-新增序列化器
    """

    class Meta:
        model = ProductionWork
        fields = "__all__"
        read_only_fields = ["id"]


class IpcProductionWorkUpdateSerializer(CustomModelSerializer):
    """
    码包模板管理-更新列化器
    """

    class Meta:
        model = ProductionWork
        fields = '__all__'


class ProductionWorkViewSet(CustomModelViewSet):
    """
    码包模板管理接口:
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
            return ErrorResponse(msg="未获取生产工单号")
        if code_pack_id is None:
            return ErrorResponse(msg="未获取码包号")
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
                serializer=IpcProductionWorkCreateSerializer(create_data,many=False,request=request)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return DetailResponse(data=serializer.data)

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