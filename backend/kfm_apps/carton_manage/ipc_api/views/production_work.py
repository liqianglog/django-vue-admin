# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from rest_framework import serializers

from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from kfm_apps.carton_manage.code_manage.models import CodePackage
from kfm_apps.carton_manage.production_manage.models import ProductionWork


class ProductionWorkSerializer(CustomModelSerializer):
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


class ProductionWorkCreateSerializer(CustomModelSerializer):
    """
    码包模板管理-新增序列化器
    """

    class Meta:
        model = ProductionWork
        fields = "__all__"
        read_only_fields = ["id"]


class ProductionWorkUpdateSerializer(CustomModelSerializer):
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
    serializer_class = ProductionWorkSerializer
    create_serializer_class = ProductionWorkCreateSerializer
    update_serializer_class = ProductionWorkUpdateSerializer

    """
    def bind_code_package(self, request, *args, **kwargs):
        #码包绑定
        data = request.data
        work_no = data.get('work_no')
        code_pack_id= data.get('code_pack_id')
        if work_no is None:
            return ErrorResponse(msg="未获取生产工单号")
        if code_pack_id is None:
            return ErrorResponse(msg="未获取码包号")
        else:
            code_package_instance = CodePackage.objects.filter(id=code_pack_id).first()
            if code_package_instance is None:
                return ErrorResponse(msg="未查询到码包号")
            else:
                # TODO 获取设备的一些心想
                create_data = {
                    "no":work_no,
                    "code_package":code_pack_id,
                    "order_id":code_package_instance.order_id
                }
                
    """