# -*- coding: utf-8 -*-
import mimetypes
import os
import posixpath
import re
from wsgiref.util import FileWrapper

from django.db.models import Q
from django.http import Http404, HttpResponseNotModified, StreamingHttpResponse, HttpResponseBadRequest
from django.utils._os import safe_join
from django.views.static import was_modified_since
from rest_framework import serializers
from rest_framework.decorators import action

from basics_manage.models import CodePackageFormat
from carton_manage.production_manage.models import ProductionWork
from carton_manage.verify_manage.models import BackHaulFile, CameraManage
from carton_manage.verify_manage.tasks import back_haul_file_check
from dvadmin.utils.json_response import DetailResponse
from dvadmin.utils.request_util import get_request_ip
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from utils.currency import get_back_haul_file_path, md5_file
from utils.permission import DeviceManagePermission


class IpcBackHaulFileCreateSerializer(CustomModelSerializer):
    """
    回传文件管理-新增序列化器
    """

    class Meta:
        model = BackHaulFile
        fields = "__all__"
        read_only_fields = ["id"]


class IpcBackHaulFileUpdateSerializer(CustomModelSerializer):
    """
    回传文件管理-更新列化器
    """

    class Meta:
        model = BackHaulFile
        fields = '__all__'


class IpcBackHaulFileViewSet(CustomModelViewSet):
    """
    回传文件管理接口:
    """
    queryset = BackHaulFile.objects.all()
    create_serializer_class = IpcBackHaulFileCreateSerializer
    update_serializer_class = IpcBackHaulFileUpdateSerializer
    permission_classes = [DeviceManagePermission]

    def data_upload(self, request, *args, **kwargs):
        work_no = request.META.get('HTTP_WORK_NO', '').strip()
        file_name = request.META.get('HTTP_FILENAME', '').strip()
        dataformat = request.META.get('HTTP_DATAFORMAT', '').strip()  # 模板格式
        cam_id = request.META.get('HTTP_CAMID', '').strip()  # 相机ID
        zipfile_md5 = request.META.get('HTTP_ZIPFILEMD5', '').strip()  # zip文件md5
        key_id = request.META.get('HTTP_KEYID', '').strip()  # zip文件md5

        if work_no is None:
            ret = HttpResponseBadRequest('未获取到生产工单号')
            ret["STATUS-CODE"] = 400
            return ret
        device = request.user.device_id
        production_work_obj = ProductionWork.objects.filter(no=work_no, device__id=device).first()
        if production_work_obj is None:
            ret = HttpResponseBadRequest('非当前设备的生产工单')
            ret["STATUS-CODE"] = 400
            return ret

        code_package_format_obj = CodePackageFormat.objects.filter(no=dataformat).first()
        if not code_package_format_obj:
            ret = HttpResponseBadRequest('检测回传码包格式不存在')
            ret["STATUS-CODE"] = 400
            return ret

        # 获取保存文件目录
        path = posixpath.normpath(os.path.join(get_back_haul_file_path(), work_no, cam_id))
        file_path = posixpath.normpath(os.path.join(path, file_name))
        if not os.path.exists(path):  # 文件夹不存在则创建
            os.makedirs(path)
        # 保存文件
        file = request.FILES.get('file')
        # file_split = os.path.splitext(str(file))
        # print(file_split)
        with open(file_path, 'wb') as fp:  # 写文件
            for i in file.chunks():
                fp.write(i)
        # 1. 校验MD5值
        # 2. 保存数据到上传记录中
        # 3. 发行到异步任务中，进行异步处理
        new_zipfile_md5 = md5_file(file_path)
        if new_zipfile_md5 != zipfile_md5:
            if production_work_obj is None:
                ret = HttpResponseBadRequest('文件错误，与上传MD5值不符')
                ret["STATUS-CODE"] = 400
                return ret
        # 更新相机管理内容
        cam_obj, _ = CameraManage.objects.get_or_create(
            no=cam_id, device_id=device,
            defaults={
                "creator": self.request.user,
                "modifier": self.request.user.id,
                "dept_belong_id": self.request.user.dept
            })
        # 保存数据到上传记录中
        data = {
            "production_work": production_work_obj.id,
            "device": device,
            "cam": cam_obj.id,
            "file_position": os.path.join(work_no, cam_id, file_name),
            "file_md5": zipfile_md5,
            "key_id": key_id,
            "code_package_format": code_package_format_obj.id

        }
        serializer = self.create_serializer_class(data=data, request=request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # 进行异步校验
        back_haul_file_check.delay(back_haul_file_id=serializer.data.get('id'))
        return DetailResponse(data=None, msg="上传成功")
