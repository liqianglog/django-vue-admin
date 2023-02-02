# -*- coding: utf-8 -*-
from carton_manage.production_manage.models import ProductionWorkStatusRecord
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class IpcProductionWorkStatusRecordSerializer(CustomModelSerializer):
    """
    生产状态记录-序列化器
    """
 
    class Meta:
        model = ProductionWorkStatusRecord
        fields = "__all__"
        read_only_fields = ["id"]


class IpcProductionWorkStatusRecordCreateSerializer(CustomModelSerializer):
    """
    生产状态记录-新增序列化器
    """

    class Meta:
        model = ProductionWorkStatusRecord
        fields = "__all__"
        read_only_fields = ["id"]


class IpcProductionWorkStatusRecordUpdateSerializer(CustomModelSerializer):
    """
    生产状态记录-更新列化器
    """

    class Meta:
        model = ProductionWorkStatusRecord
        fields = '__all__'


class ProductionWorkStatusRecordViewSet(CustomModelViewSet):
    """
    生产状态记录接口:
    """
    queryset = ProductionWorkStatusRecord.objects.all()
    serializer_class = IpcProductionWorkStatusRecordSerializer
    create_serializer_class = IpcProductionWorkStatusRecordCreateSerializer
    update_serializer_class = IpcProductionWorkStatusRecordUpdateSerializer