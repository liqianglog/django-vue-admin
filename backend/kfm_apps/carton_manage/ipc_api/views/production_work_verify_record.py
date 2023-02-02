# -*- coding: utf-8 -*-
from carton_manage.production_manage.models import ProductionWorkVerifyRecord
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class IpcProductionWorkVerifyRecordSerializer(CustomModelSerializer):
    """
    生产校验-序列化器
    """
 
    class Meta:
        model = ProductionWorkVerifyRecord
        fields = "__all__"
        read_only_fields = ["id"]


class IpcProductionWorkVerifyRecordCreateSerializer(CustomModelSerializer):
    """
    生产校验-新增序列化器
    """

    class Meta:
        model = ProductionWorkVerifyRecord
        fields = "__all__"
        read_only_fields = ["id"]


class IpcProductionWorkVerifyRecordUpdateSerializer(CustomModelSerializer):
    """
    生产校验-更新列化器
    """

    class Meta:
        model = ProductionWorkVerifyRecord
        fields = '__all__'


class ProductionWorkVerifyRecordViewSet(CustomModelViewSet):
    """
    生产校验接口:
    """
    queryset = ProductionWorkVerifyRecord.objects.all()
    serializer_class = IpcProductionWorkVerifyRecordSerializer
    create_serializer_class = IpcProductionWorkVerifyRecordCreateSerializer
    update_serializer_class = IpcProductionWorkVerifyRecordUpdateSerializer