import mimetypes
import os
import posixpath
import re
from _pydecimal import Decimal
from wsgiref.util import FileWrapper
from urllib.parse import quote

from django.db.models import IntegerField, Sum, Q, Count
from django.db.models.functions import Coalesce
from django.http import HttpResponseBadRequest, HttpResponseNotModified, StreamingHttpResponse
from django.utils._os import safe_join
from django.views.static import was_modified_since
from rest_framework import serializers
from rest_framework.decorators import action

from carton_manage.verify_manage.models import BackHaulFile, VerifyCodeRecord
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from utils.currency import get_back_haul_file_path


class BackHaulFileSerializer(CustomModelSerializer):
    """
   回传文件管理-序列化器
    """
    device_name = serializers.CharField(source='device.name', read_only=True)
    prod_line_name = serializers.CharField(source='device.production_line.name', read_only=True)
    factory_name = serializers.CharField(source='device.production_line.belong_to_factory.name', read_only=True)
    success_rate = serializers.SerializerMethodField(help_text="识别成功率")
    cam_no = serializers.CharField(source='cam.no', read_only=True)

    def get_success_rate(self, instance):
        total_number = instance.total_number
        success_number = instance.success_number
        if total_number == 0:
            return '0'
        else:
            rate = success_number / total_number * 100
            return str(Decimal(rate).quantize(Decimal('0.00')))

    class Meta:
        model = BackHaulFile
        fields = "__all__"
        read_only_fields = ["id"]


class BackHaulFileCreateUpdateSerializer(CustomModelSerializer):
    """
   回传文件管理管理 创建/更新时的列化器
    """

    class Meta:
        model = BackHaulFile
        fields = '__all__'


class BackHaulFileViewSet(CustomModelViewSet):
    """
   回传文件管理管理接口:
    """
    queryset = BackHaulFile.objects.all()
    serializer_class = BackHaulFileSerializer
    create_serializer_class = BackHaulFileCreateUpdateSerializer
    update_serializer_class = BackHaulFileCreateUpdateSerializer

    @action(methods=['get'], detail=True)
    def download_file(self, request, pk, **kwargs):
        """
        # 基于django.views.static.serve实现，支持大文件的断点续传（暂停/继续下载）
        """
        _BackHaulFile = BackHaulFile.objects.filter(id=pk).first()
        if _BackHaulFile is None:
            ret = HttpResponseBadRequest('未获取到回传文件')
            ret["STATUS-CODE"] = 400
            return ret
        # 防止目录遍历漏洞
        file_position = _BackHaulFile.file_position
        fullpath = os.path.join(get_back_haul_file_path(), file_position)
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
            response["content-disposition"] = f'attachment;filename={quote(str(f"{_BackHaulFile.file_name}"))}'
            return response
