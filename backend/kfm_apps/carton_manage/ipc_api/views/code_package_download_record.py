# -*- coding: utf-8 -*-
from carton_manage.production_manage.models import CodePackageDownloadRecord
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class IpcCodePackageDownloadRecordSerializer(CustomModelSerializer):
    """
    生产状态记录-序列化器
    """

    class Meta:
        model = CodePackageDownloadRecord
        fields = "__all__"
        read_only_fields = ["id"]


class IpcCodePackageDownloadRecordCreateSerializer(CustomModelSerializer):
    """
    生产状态记录-新增序列化器
    """

    class Meta:
        model = CodePackageDownloadRecord
        fields = "__all__"
        read_only_fields = ["id"]


class IpcCodePackageDownloadRecordUpdateSerializer(CustomModelSerializer):
    """
    生产状态记录-更新列化器
    """

    class Meta:
        model = CodePackageDownloadRecord
        fields = '__all__'


class CodePackageDownloadRecordViewSet(CustomModelViewSet):
    """
    生产状态记录接口:
    """
    queryset = CodePackageDownloadRecord.objects.all()
    serializer_class = IpcCodePackageDownloadRecordSerializer
    create_serializer_class = IpcCodePackageDownloadRecordCreateSerializer
    update_serializer_class = IpcCodePackageDownloadRecordUpdateSerializer