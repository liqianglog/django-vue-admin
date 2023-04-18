# -*- coding: utf-8 -*-
from rest_framework import serializers

from carton_manage.code_manage.models import CodeRepetitionRecord
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class CodeRepetitionRecordSerializer(CustomModelSerializer):
    """
    码包管理-序列化器
    """
    code_package_no = serializers.CharField(source='code_package.no', read_only=True)
    code_package_order_id = serializers.CharField(source='code_package.order_id', read_only=True)
    repetition_code_package_no = serializers.CharField(source='repetition_code_package.no', read_only=True)
    repetition_code_package_order_id = serializers.CharField(source='repetition_code_package.order_id', read_only=True)

    class Meta:
        model = CodeRepetitionRecord
        fields = "__all__"
        read_only_fields = ["id"]


class CodeRepetitionRecordCreateSerializer(CustomModelSerializer):
    """
    码包管理-新增序列化器
    """

    class Meta:
        model = CodeRepetitionRecord
        fields = "__all__"
        read_only_fields = ["id"]


class CodeRepetitionRecordUpdateSerializer(CustomModelSerializer):
    """
    码包管理-更新列化器
    """

    class Meta:
        model = CodeRepetitionRecord
        fields = '__all__'


class CodeRepetitionRecordExportSerializer(CustomModelSerializer):
    """
    码包管理-序列化器
    """
    code_package_no = serializers.CharField(source='code_package.no', read_only=True)
    code_package_order_id = serializers.CharField(source='code_package.order_id', read_only=True)
    repetition_code_package_no = serializers.CharField(source='repetition_code_package.no', read_only=True)
    repetition_code_package_order_id = serializers.CharField(source='repetition_code_package.order_id', read_only=True)
    repetition_type = serializers.CharField(source='get_repetition_type_display',read_only=True)

    class Meta:
        model = CodeRepetitionRecord
        fields = "__all__"
        read_only_fields = ["id"]

class CodeRepetitionRecordViewSet(CustomModelViewSet):
    """
    码包管理接口:
    """
    queryset = CodeRepetitionRecord.objects.all()
    serializer_class = CodeRepetitionRecordSerializer
    create_serializer_class = CodeRepetitionRecordCreateSerializer
    update_serializer_class = CodeRepetitionRecordUpdateSerializer
    export_serializer_class = CodeRepetitionRecordExportSerializer
    export_field_label = {
        "code_package_order_id": "重码订单编号",
        "code_package_no":"重码码包编号",
        "code_content":"码内容",
        "code_type":"码类型",
        "repetition_code_package_order_id": "重码订单编号",
        "repetition_code_package_no": "重码码包编号",
        "repetition_type":"重码类型"
    }
