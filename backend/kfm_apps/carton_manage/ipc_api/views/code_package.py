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

from carton_manage.production_manage.models import ProductionWork
from dvadmin.utils.json_response import DetailResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from carton_manage.code_manage.models import CodePackage
from utils.permission import DeviceManagePermission


class IpcCodePackageSerializer(CustomModelSerializer):
    """
    码包管理-序列化器
    """
    code_pack_id = serializers.IntegerField(source="id", read_only=True)
    code_pack_name = serializers.CharField(source="no", read_only=True)
    package_template_no = serializers.CharField(source="code_package_template.no", read_only=True)

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


class IpcCodePackageCreateSerializer(CustomModelSerializer):
    """
    码包管理-新增序列化器
    """

    class Meta:
        model = CodePackage
        fields = "__all__"
        read_only_fields = ["id"]


class IpcCodePackageUpdateSerializer(CustomModelSerializer):
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
    serializer_class = IpcCodePackageSerializer
    create_serializer_class = IpcCodePackageCreateSerializer
    update_serializer_class = IpcCodePackageUpdateSerializer
    permission_classes = [DeviceManagePermission]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset \
            .filter(device_manage_id__isnull=True) \
            .filter(validate_status=4) \
            .filter(Q(work_code_package__isnull=True) | Q(work_code_package__status=0))
        serializer = IpcCodePackageSerializer(queryset, many=True)
        return DetailResponse(data=serializer.data)

    def download_code_package_file(self, request, *args, **kwargs):
        """
        # 基于django.views.static.serve实现，支持大文件的断点续传（暂停/继续下载）
        """
        work_no = request.META.get('HTTP_WORK_NO', '').strip()
        if work_no is None:
            ret = HttpResponseBadRequest('未获取到生产工单号')
            ret["STATUS-CODE"] = 400
            return ret
        device = request.user.device_id
        _ProductionWork = ProductionWork.objects.filter(no=work_no,device__id=device).first()
        if _ProductionWork is None:
            ret = HttpResponseBadRequest('非当前设备的生产工单')
            ret["STATUS-CODE"] = 400
            return ret
        # 防止目录遍历漏洞
        path = posixpath.normpath(
            os.path.join(kwargs.get('tenant_name'), kwargs.get('day'), kwargs.get('file_name'))).lstrip('/')
        print(path)
        fullpath = safe_join('kfm_code_file/code_package_txt_file', path)
        if os.path.isdir(fullpath):
            ret = HttpResponseBadRequest('这里不允许使用目录索引')
            ret["STATUS-CODE"] = 400
            return ret
        if not os.path.exists(fullpath):
            ret = HttpResponseBadRequest('"%(path)s" 不存在' % {'path': fullpath})
            ret["STATUS-CODE"] = 400
            return ret
        statobj = os.stat(fullpath)
        # 判断下载过程中文件是否被修改过
        if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                                  statobj.st_mtime, statobj.st_size):
            ret = HttpResponseNotModified()
            ret["STATUS-CODE"] = 304
            return ret

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
            response["STATUS-CODE"] = 200
            response.status_code = 206
            return response
        else:
            response = StreamingHttpResponse(FileWrapper(open(fullpath, 'rb'), 8192), content_type=content_type)
            response['Content-Length'] = str(size)
            response['Accept-Ranges'] = 'bytes'
            response["STATUS-CODE"] = 200
            return response
