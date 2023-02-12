# -*- coding: utf-8 -*-
from carton_manage.verify_manage.models import VerifyWorkOrderStatusRecord
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class IpcVerifyWorkOrderStatusRecordSerializer(CustomModelSerializer):
    """
    检测状态记录-序列化器
    """

    class Meta:
        model = VerifyWorkOrderStatusRecord
        fields = "__all__"
        read_only_fields = ["id"]


class IpcVerifyWorkOrderStatusRecordCreateSerializer(CustomModelSerializer):
    """
    检测状态记录-新增序列化器
    """

    class Meta:
        model = VerifyWorkOrderStatusRecord
        fields = "__all__"
        read_only_fields = ["id"]


class IpcVerifyWorkOrderStatusRecordUpdateSerializer(CustomModelSerializer):
    """
    检测状态记录-更新列化器
    """

    class Meta:
        model = VerifyWorkOrderStatusRecord
        fields = '__all__'


class VerifyWorkOrderStatusRecordViewSet(CustomModelViewSet):
    """
    检测状态记录接口:
    """
    queryset = VerifyWorkOrderStatusRecord.objects.all()
    serializer_class = IpcVerifyWorkOrderStatusRecordSerializer
    create_serializer_class = IpcVerifyWorkOrderStatusRecordCreateSerializer
    update_serializer_class = IpcVerifyWorkOrderStatusRecordUpdateSerializer
