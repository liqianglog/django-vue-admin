# -*- coding: utf-8 -*-
import random
import shutil
import zipfile

from django.db import transaction
from rest_framework import serializers
from rest_framework.decorators import action

from application import settings
from basics_manage.models import CodePackageTemplate
from dvadmin.utils.json_response import ErrorResponse, SuccessResponse, DetailResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from carton_manage.code_manage.models import CodePackage
from utils.currency import unzip_compress_file
import os
from utils.currency import get_code_package_import_zip_path, check_zip_is_encrypted, file_now_datetime, zip_is_txt, \
    get_code_package_import_txt_path, read_max_row, md5_file, md5_value, read_file_first

from carton_manage.code_manage.tasks import code_package_import_check


class CodePackageSerializer(CustomModelSerializer):
    """
    码包管理-序列化器
    """
    code_type_label = serializers.CharField(source="get_code_type_display", read_only=True)
    source_label = serializers.CharField(source="get_source_display", read_only=True)

    class Meta:
        model = CodePackage
        exclude =['import_log']
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
        folder_abs = get_code_package_import_zip_path()
        file_path = os.path.join(folder_abs, file_now_datetime())
        if not os.path.exists(file_path):  # 文件夹不存在则创建
            os.makedirs(file_path)
        with open(os.path.join(file_path, file.name), 'wb') as fp:  # 写文件
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
        data = {"file_path": os.path.join(file_now_datetime(), file.name), "name": name, "is_encrypted": is_encrypted,
                "file_type": file_type}
        return SuccessResponse(data=data, msg="上传成功")

    @action(methods=['POST'], detail=False, permission_classes=[])
    def create_code_package_info(self, request):
        """
        创建码包订单信息
        1.获取文件,判断是ZIP还是TXT格式
        1.1.如果是ZIP需要解压缩,获取里面的TXT文件
        1.1.1.判断是否有加密,如有加密,需要解密密码
        1.1.2 判断是否解压后,都是TXT文件
        1.2.如果是TXT,则存入码文件库
        """
        data = request.data
        file_type = data.get("file_type")
        file_path = os.path.join(get_code_package_import_zip_path(), data.get("file_path"))
        if not os.path.exists(file_path):
            return ErrorResponse(code=2104, data=None, msg="文件不存在,请重新上传!")
        pwd = data.get('pwd', None) and data.get('pwd', None).encode("utf-8")
        file_now_date = file_now_datetime()
        txt_file_path = os.path.join(get_code_package_import_txt_path(), file_now_date)
        if file_type == "zip":
            # 指定解压的目录
            with zipfile.ZipFile(file_path, allowZip64=True) as zip_file:
                file_name_list = zip_file.namelist()  # 得到压缩包里所有文件
                file_name_list = [ele for ele in file_name_list if not ele.startswith("_")]
                is_txt = zip_is_txt(file_name_list)  # 判断是否全是txt文件
                if not is_txt:
                    return ErrorResponse(code=2101, msg="zip包中内部文件格式不正确")
                try:
                    with zip_file.open(zip_file.namelist()[0], pwd=pwd) as myfile:  # 得到压缩包里所有文件
                        myfile.readline()
                except Exception as e:
                    print("zip文件密码错误", e)
                    return ErrorResponse(code=2101, msg="zip文件密码错误")
                # 进行解压文件
                unzip_compress_file(file_path, txt_file_path, is_rm=False, pwd=pwd,
                                    specify_file_name=file_name_list)
            os.remove(file_path)  # 删除zip包
        elif file_type == "txt":
            new_file_path = os.path.join(txt_file_path, str(file_path.split(os.sep)[-1]))
            shutil.move(file_path, new_file_path)
            file_name_list = [new_file_path]
        else:
            return ErrorResponse(code=2101, msg="文件类型错误")
        code_package_template_obj = CodePackageTemplate.objects.filter(id=data.get('code_package_template')).first()
        if not code_package_template_obj:
            return ErrorResponse(msg="码包模板不存在!")
        code_package_id_list = []
        with transaction.atomic():
            for file_name in file_name_list:
                print("file_name", file_name)
                txt_file = os.path.join(txt_file_path, file_name)
                first_line_md5 = md5_value(read_file_first(txt_file))  # 文件首行MD5值
                total_number = read_max_row(txt_file).get('count')  # 文件总行数
                file_md5 = md5_file(txt_file)  # 文件MD5 值
                # 校验文件是否重复
                code_package_data = {
                    "zip_name": data.get("file_path").split(os.sep)[-1],
                    "no": file_name.strip('.txt'),
                    "order_id": data.get("order_id"),
                    "product_name": data.get("product_name"),
                    "arrival_factory": data.get("arrival_factory"),
                    "total_number": total_number,
                    "code_package_template": data.get('code_package_template'),
                    "code_type": code_package_template_obj.code_type,
                    "key_id": settings.ENCRYPTION_KEY_ID.index(random.choice(settings.ENCRYPTION_KEY_ID)),
                    "file_position": os.path.join(file_now_date, file_name),
                    "file_md5": file_md5,
                    "first_line_md5": first_line_md5,
                }
                # # 保存码包信息
                code_package_serializer = CodePackageCreateSerializer(data=code_package_data, many=False,
                                                                      request=request)
                if not code_package_serializer.is_valid(raise_exception=True):
                    return ErrorResponse(code=2101, data=None, msg=code_package_serializer.error_messages)
                code_package_serializer.save()
                code_package_id_list.append(code_package_serializer.instance.id)
                print("码包信息ID", code_package_serializer.instance.id)
        code_package_import_check.delay(code_package_ids=code_package_id_list)
        return SuccessResponse(data=None, msg="正在导入中...")

    @action(methods=['get'], detail=True, permission_classes=[])
    def view_log(self,request,pk):
        _CodePackage = CodePackage.objects.filter(id=pk).first()
        print(_CodePackage.import_log)
        if _CodePackage is None:
            return DetailResponse(data=None)
        else:
            return DetailResponse(data=_CodePackage.import_log)
