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

from basics_manage.models import CodePackageFormat, DeviceManage
from carton_manage.ipc_api.views.production_work_status_record import IpcProductionWorkStatusRecordCreateSerializer
from carton_manage.ipc_api.views.verify_work_order_status_record import IpcVerifyWorkOrderStatusRecordCreateSerializer
from carton_manage.production_manage.models import ProductionWork
from carton_manage.verify_manage.models import BackHaulFile, CameraManage, VerifyWorkOrder
from carton_manage.verify_manage.tasks import back_haul_file_check
from carton_manage.verify_manage.views.verify_work_order import VerifyWorkOrderCreateSerializer
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
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
        verify_no = request.META.get('HTTP_VERIFY_NO', '').strip()
        file_name = request.META.get('HTTP_FILENAME', '').strip()
        dataformat = request.META.get('HTTP_DATAFORMAT', '').strip()  # 模板格式
        cam_id = request.META.get('HTTP_CAMID', '').strip()  # 相机ID
        zipfile_md5 = request.META.get('HTTP_ZIPFILEMD5', '').strip()  # zip文件md5
        key_id = request.META.get('HTTP_KEYID', '').strip()  # zip文件md5

        if verify_no is None:
            ret = HttpResponseBadRequest('未获取到检测生产工单号')
            ret["STATUS-CODE"] = 400
            return ret
        device = request.user.device_id
        verify_work_order_obj = VerifyWorkOrder.objects.filter(no=verify_no).first()
        if verify_work_order_obj:
            if verify_work_order_obj.device_id != device:
                ret = HttpResponseBadRequest('非当前设备的检测生产工单')
                ret["STATUS-CODE"] = 400
                return ret
        else:
            # 创建检测生产工单
            device_manage_obj = DeviceManage.objects.filter(id=device).first()
            data = {
                "no": verify_no,
                "production_work_no": None,
                "device": device,
                "production_line": device_manage_obj.production_line.id,
                "factory_info": device_manage_obj.production_line.belong_to_factory.id,
            }
            serializer = VerifyWorkOrderCreateSerializer(data=data, request=request)
            serializer.is_valid(raise_exception=True)
            serializer.save()


        code_package_format_obj = CodePackageFormat.objects.filter(no=dataformat).first()
        if not code_package_format_obj:
            ret = HttpResponseBadRequest('检测回传码包格式不存在')
            ret["STATUS-CODE"] = 400
            return ret
        # 获取保存文件目录
        path = posixpath.normpath(os.path.join(get_back_haul_file_path(), verify_no, cam_id))
        file_path = posixpath.normpath(os.path.join(path, file_name))
        if not os.path.exists(path):  # 文件夹不存在则创建
            os.makedirs(path)
        # 保存文件
        with open(file_path, 'wb') as fp:  # 写文件
            fp.write(request.body)
        # 1. 校验MD5值
        # 2. 保存数据到上传记录中
        # 3. 发行到异步任务中，进行异步处理
        new_zipfile_md5 = md5_file(file_path)
        if new_zipfile_md5 != zipfile_md5:
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
            "verify_work_no": verify_work_order_obj.no,
            "device": device,
            "cam": cam_obj.id,
            "file_position": os.path.join(verify_no, cam_id, file_name),
            "file_md5": zipfile_md5,
            "key_id": key_id,
            "file_name": file_name,
            "code_package_format": code_package_format_obj.id

        }
        serializer = self.create_serializer_class(data=data, request=request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # 进行异步校验
        back_haul_file_check.delay(back_haul_file_id=serializer.data.get('id'))
        return DetailResponse(data=None, msg="上传成功")

    def verify_status_change(self, request):
        # 生产工单变化
        data = request.data
        verify_no = data.get('verify_no', None)
        verify_status = data.get('verify_status', None)
        if verify_no is None:
            return ErrorResponse(msg="未获取到检测生产工单号")
        verify_work_order_instance = VerifyWorkOrder.objects.filter(no=verify_no).first()
        device = request.user.device_id
        if verify_work_order_instance is None:
            # 创建检测生产工单
            device_manage_obj = DeviceManage.objects.filter(id=device).first()
            data = {
                "no": verify_no,
                "production_work_no": None,
                "device": device,
                "production_line": device_manage_obj.production_line.id,
                "factory_info": device_manage_obj.production_line.belong_to_factory.id,
            }
            serializer = VerifyWorkOrderCreateSerializer(data=data, request=request)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        if verify_status is None:
            return ErrorResponse(msg="未获取到检测状态")
        verify_work_order_instance.verify_status = verify_status
        verify_work_order_instance.save()
        # *************加入生产状态记录***************#
        create_data = {
            "production_work": verify_work_order_instance.id,
            "status": verify_status
        }
        serializer = IpcVerifyWorkOrderStatusRecordCreateSerializer(data=create_data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # *************加入检测状态记录表***************#
        return DetailResponse(msg="更新成功")

    def check_file_upload_all(self, request):
        """
        检测端校验文件是否全部已上传
        """
        data = request.data
        file_list = data.get('file_list', [])
        verify_no = data.get('verify_no', None)
        if verify_no is None:
            return ErrorResponse(msg="未获取到生产工单号")
        if not file_list:
            return ErrorResponse(msg="文件列表不能为空")
        db_file_list = BackHaulFile.objects.filter(verify_work_order=verify_no, file_name__in=file_list).values_list(
            'file_name', flat=True)
        # 未上传的文件列表
        not_upload_file_list = list(set(file_list) - set(db_file_list))

        return DetailResponse(data={"not_upload_file_list": not_upload_file_list}, msg="获取成功")
