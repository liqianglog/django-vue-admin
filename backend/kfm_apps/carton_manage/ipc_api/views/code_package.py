# -*- coding: utf-8 -*-
import mimetypes
import os
import posixpath
import re
from wsgiref.util import FileWrapper

from django.http import Http404, HttpResponseNotModified, StreamingHttpResponse
from django.utils._os import safe_join
from django.views.static import was_modified_since
from rest_framework import serializers
from rest_framework.decorators import action

from dvadmin.utils.json_response import DetailResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from carton_manage.code_manage.models import CodePackage


class IpcCodePackageSerializer(CustomModelSerializer):
    """
    码包管理-序列化器
    """
    code_pack_id = serializers.IntegerField(source="id",read_only=True)
    code_pack_name = serializers.CharField(source="no",read_only=True)
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
    permission_classes = []

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer=IpcCodePackageSerializer(queryset,many=True)
        return DetailResponse(data=serializer.data)

@action(methods=['get'], detail=False, permission_classes=[])
    # 基于django.views.static.serve实现，支持大文件的断点续传（暂停/继续下载）
def download_code_package_file(request,path):
    # 防止目录遍历漏洞
    path = posixpath.normpath(path).lstrip('/')
    print(path)
    fullpath = safe_join('kfm_code_file/code_package_txt_file', path)
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