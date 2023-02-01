# -*- coding: utf-8 -*-
from carton_manage.code_manage.models import CodeRepetitionRecord
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class CodeRepetitionRecordSerializer(CustomModelSerializer):
    """
    码包管理-序列化器
    """
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


class CodeRepetitionRecordViewSet(CustomModelViewSet):
    """
    码包管理接口:
    """
    queryset = CodeRepetitionRecord.objects.all()
    serializer_class = CodeRepetitionRecordSerializer
    create_serializer_class = CodeRepetitionRecordCreateSerializer
    update_serializer_class = CodeRepetitionRecordUpdateSerializer
