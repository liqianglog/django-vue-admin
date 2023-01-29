# -*- coding: utf-8 -*-
import os
import time

from rest_framework.decorators import action

from dvadmin.utils.json_response import ErrorResponse, SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from carton_manage.code_manage.models import CodePackage
from utils.currency import get_code_package_import_path, check_zip_is_encrypted, file_now_datetime


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
        folder_abs = get_code_package_import_path()
        file_path = os.path.join(folder_abs, file_now_datetime(), file.name)
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
        body = request.data
        file_type = body.get("file_type")
        file_path = os.path.join(get_code_package_import_path(), body.get("file_path"))
        if not os.path.exists(file_path):
            return ErrorResponse(code=2104, data=None, msg="文件不存在,请重新上传!")
        brand_owner = body.get("brand_owner")
        file_md5_path = f"{str(time.time()).replace('.', '')}{random.randint(1000, 9999)}"
        pwd = body.get('pwd', None) and body.get('pwd', None).encode("utf-8")
        if file_type == "zip":
            # 指定解压的目录
            zip_file = zipfile.ZipFile(file_path)  # 实例化zip压缩包对象
            try:
                with zip_file.open(zip_file.namelist()[0], pwd=pwd) as myfile:  # 得到压缩包里所有文件
                    myfile.readline()
            except:
                print("zip文件密码错误")
                return ErrorResponse(code=2103, msg="zip文件密码错误")
        brandOwnerOrderData = {
            "id": body.get("id"),
            "name": body.get("name"),
            "brand_owner": brand_owner,
            "file": file_md5_path,
            "log": None
        }
        #### 获取所有的txt文件，如果为单txt 文件，则移动到相应目录下
        # 保存订单
        brand_owner_order_serializer = BrandOwnerOrdersSerializer(data=brandOwnerOrderData, many=False, request=request)
        if not brand_owner_order_serializer.is_valid(raise_exception=True):
            return ErrorResponse(code=2101, data=None, msg=brand_owner_order_serializer.error_messages)
        brand_owner_order_serializer.save()

        order_file_import_check.delay(brand_owner_order_id=brand_owner_order_serializer.instance.id,
                                      file_type=file_type,
                                      file_path=file_path,
                                      pwd=body.get('pwd', None),
                                      username=self.request.user.username)
        return SuccessResponse(data=None, msg="正在导入中...")
