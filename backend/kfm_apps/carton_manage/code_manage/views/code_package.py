# -*- coding: utf-8 -*-
import os

from rest_framework import serializers
from rest_framework.decorators import action

from dvadmin.utils.json_response import DetailResponse, ErrorResponse, SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from carton_manage.code_manage.models import CodePackage
from utils.currency import get_order_import_path, check_zip_is_encrypted


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

    @action(methods=['POST'], detail=False, permission_classes=[])
    def upload_file(self, request, *args, **kwargs):
        """
        上传码包文件
        request:
        """
        file = request.FILES.get('file')
        file_split = os.path.splitext(str(file))
        name = file_split[0]
        file_suffix = file_split[1]
        folder_abs = get_order_import_path()
        file_path = os.path.join(folder_abs, file.name)
        with open(file_path, 'wb') as fp:  # 写文件
            for i in file.chunks():
                fp.write(i)

        is_encrypted = False
        file_suffix = file_suffix.lower()
        if file_suffix == ".zip":
            file_type = "zip"
            is_encrypted = check_zip_is_encrypted(file)  # 判断ZIP是否加密
        elif file_suffix == ".txt":
            file_type = "txt"
        else:
            return ErrorResponse(code=2100, data=None, msg="文件格式不正确")
        data = {"file_path": file.name, "name": name, "is_encrypted": is_encrypted, "file_type": file_type}
        return SuccessResponse(data=data, msg="上传成功")
