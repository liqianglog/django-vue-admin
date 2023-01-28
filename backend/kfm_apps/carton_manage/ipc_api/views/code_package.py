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
    code_pack_id = serializers.IntegerField(source="id",read_only=True)
    code_pack_name = serializers.CharField(source="no",read_only=True)
    # "code_type": 1,
    package_template_no = serializers.CharField(source="code_package_template.no",read_only=True)

    class Meta:
        model = CodePackage
        fields = [
            'code_pack_id',
            'code_pack_name',
            'total_number',
            'arrival_factory',
            'product_name',
            'package_template_no',
            'order_id',
            'code_type'
        ]
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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer=CodePackageSerializer(queryset,many=True)
        return DetailResponse(data=serializer.data)
