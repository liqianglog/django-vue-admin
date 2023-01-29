# -*- coding: utf-8 -*-
from rest_framework import serializers

from dvadmin.utils.json_response import DetailResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from carton_manage.code_manage.models import CodePackage


class CodePackageSerializer(CustomModelSerializer):
    """
    码包管理-序列化器
    """
    class Meta:
        model = CodePackage
        fields = "__all__"
        read_only_fields = ["id"]


class CodePackageCreateSerializer(CustomModelSerializer):
    """
    码包管理-新增序列化器
    """
    class Meta:
        model = CodePackage
        fields = "__all__"
        read_only_fields = ["id"]


class CodePackageUpdateSerializer(CustomModelSerializer):
    """
    码包管理-更新列化器
    """

    class Meta:
        model = CodePackage
        fields = '__all__'


class CodePackageViewSet(CustomModelViewSet):
    """
    码包管理接口:
    """
    queryset = CodePackage.objects.all()
    serializer_class = CodePackageSerializer
    create_serializer_class = CodePackageCreateSerializer
    update_serializer_class = CodePackageUpdateSerializer

