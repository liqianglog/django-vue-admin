# -*- coding: utf-8 -*-
import os
import random
import shutil
import time
import zipfile
from wsgiref.util import FileWrapper

from rest_framework.decorators import action

from application import settings
from basics_manage.models import CodePackageTemplate
from dvadmin.utils.json_response import ErrorResponse, SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from carton_manage.code_manage.models import CodePackage
from utils.currency import get_code_package_import_zip_path, check_zip_is_encrypted, file_now_datetime, file_iterator
import mimetypes
import os
import posixpath
import re
import stat
from utils.currency import get_code_package_import_zip_path, check_zip_is_encrypted, file_now_datetime, zip_is_txt, \
    get_code_package_import_txt_path, read_max_row, md5_file, md5_value, read_file_first

from django.http import Http404, HttpResponseNotModified, FileResponse, StreamingHttpResponse
from django.utils._os import safe_join
from django.utils.http import http_date
from django.views.static import was_modified_since
from carton_manage.code_manage.tasks import code_package_import_check
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
                    for f in file_name_list:
                        zip_file.extract(f, txt_file_path, pwd=pwd)  # 循环解压文件到指定目录
                except Exception as e:
                    print("zip文件密码错误", e)
                    return ErrorResponse(code=2101, msg="zip文件密码错误")
            # os.remove(file_path)  # 删除zip包
        elif file_type == "txt":
            new_file_path = os.path.join(txt_file_path, str(file_path.split(os.sep)[-1]))
            shutil.move(file_path, new_file_path)
            file_name_list = [new_file_path]
        else:
            return ErrorResponse(code=2101, msg="文件类型错误")
        code_package_template_obj = CodePackageTemplate.objects.filter(id=data.get('code_package_template')).first()
        if not code_package_template_obj:
            return ErrorResponse(msg="码包模板不存在!")
        for file_name in file_name_list:
            print(file_name)
            file_path = os.path.join(get_code_package_import_txt_path(), file_now_date, file_name)
            total_number = read_max_row(file_path).get('count')  # 文件总行数
            file_md5 = md5_file(file_path)  # 文件MD5 值
            first_line_md5 = md5_value(read_file_first(file_path))  # 文件首行MD5值
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
            code_package_serializer = CodePackageCreateSerializer(data=code_package_data, many=False, request=request)
            if not code_package_serializer.is_valid(raise_exception=True):
                return ErrorResponse(code=2101, data=None, msg=code_package_serializer.error_messages)
            code_package_serializer.save()
            code_package_import_check.delay(code_package_id=code_package_serializer.instance.id)
        return SuccessResponse(data=None, msg="正在导入中...")

    @action(methods=['get'], detail=False,permission_classes=[])
    # 基于django.views.static.serve实现，支持大文件的断点续传（暂停/继续下载）
    def download_file(self,request):
        path = request.query_params.get('file')
        # 防止目录遍历漏洞
        path = posixpath.normpath(path).lstrip('/')
        fullpath = safe_join('kfm_code_file/code_package_file', path)
        print(fullpath)
        if os.path.isdir(fullpath):
            raise Http404('这里不允许使用目录索引')
        if not os.path.exists(fullpath):
            raise Http404('"%(path)s" 不存在' % {'path': fullpath})

        statobj = os.stat(fullpath)

        # 判断下载过程中文件是否被修改过
        if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                                  statobj.st_mtime, statobj.st_size):
            return HttpResponseNotModified()

        # 获取客户端请求的文件部分
        range_header = request.META.get('HTTP_RANGE', '').strip()
        range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)')
        range_match = range_re.match(range_header)
        size = os.path.getsize(fullpath)
        content_type = mimetypes.guess_type(fullpath)[0] or 'application/octet-stream'
        if range_match:
            first_byte, last_byte = range_match.groups()
            first_byte = int(first_byte) if first_byte else 0
            last_byte = int(last_byte) if last_byte else size - 1
            if last_byte >= size:
                last_byte = size - 1
            length = last_byte - first_byte + 1
            response = StreamingHttpResponse(FileWrapper(open(fullpath, 'rb'), 8192), content_type=content_type)
            response['Content-Length'] = str(length)
            response['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
            response['Accept-Ranges'] = 'bytes'
            response.status_code = 206
            return response
        else:
            response = StreamingHttpResponse(FileWrapper(open(fullpath, 'rb'), 8192), content_type=content_type)
            response['Content-Length'] = str(size)
            response['Accept-Ranges'] = 'bytes'
            return response
