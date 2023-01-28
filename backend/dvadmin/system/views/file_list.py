import mimetypes
import os
import posixpath
import re
import stat

from django.http import Http404, HttpResponseNotModified, FileResponse
from django.utils._os import safe_join
from django.utils.http import http_date
from django.views.static import was_modified_since
from rest_framework import serializers
from rest_framework.decorators import action

from dvadmin.system.models import FileList
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class FileSerializer(CustomModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    def get_url(self, instance):
        return 'media/' + str(instance.url)

    class Meta:
        model = FileList
        fields = "__all__"

    def create(self, validated_data):
        validated_data['name'] = str(self.initial_data.get('file'))
        validated_data['url'] = self.initial_data.get('file')
        return super().create(validated_data)


class FileViewSet(CustomModelViewSet):
    """
    文件管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = FileList.objects.all()
    serializer_class = FileSerializer
    filter_fields = ['name', ]
    permission_classes = []

    @action(methods=['get'],detail=False)
    # 基于django.views.static.serve实现，支持大文件的断点续传（暂停/继续下载）
    def get_file_response(request, path, document_root=None):
        # 防止目录遍历漏洞
        path = posixpath.normpath(path).lstrip('/')
        fullpath = safe_join(document_root, path)
        if os.path.isdir(fullpath):
            raise Http404('Directory indexes are not allowed here.')
        if not os.path.exists(fullpath):
            raise Http404('"%(path)s" does not exist' % {'path': fullpath})

        statobj = os.stat(fullpath)

        # 判断下载过程中文件是否被修改过
        if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                                  statobj.st_mtime, statobj.st_size):
            return HttpResponseNotModified()

        # 获取文件的content_type
        content_type, encoding = mimetypes.guess_type(fullpath)
        content_type = content_type or 'application/octet-stream'

        # 计算读取文件的起始位置
        start_bytes = re.search(r'bytes=(\d+)-', request.META.get('HTTP_RANGE', ''), re.S)
        start_bytes = int(start_bytes.group(1)) if start_bytes else 0

        # 打开文件并移动下标到起始位置，客户端点击继续下载时，从上次断开的点继续读取
        the_file = open(fullpath, 'rb')
        the_file.seek(start_bytes, os.SEEK_SET)

        # status=200表示下载开始，status=206表示下载暂停后继续，为了兼容火狐浏览器而区分两种状态
        # 关于django的response对象，参考：https://www.cnblogs.com/scolia/p/5635546.html
        # 关于response的状态码，参考：https://www.cnblogs.com/DeasonGuan/articles/Hanami.html
        # FileResponse默认block_size = 4096，因此迭代器每次读取4KB数据
        response = FileResponse(the_file, content_type=content_type, status=206 if start_bytes > 0 else 200)

        # 'Last-Modified'表示文件修改时间，与'HTTP_IF_MODIFIED_SINCE'对应使用，参考：https://www.jianshu.com/p/b4ecca41bbff
        response['Last-Modified'] = http_date(statobj.st_mtime)

        # 这里'Content-Length'表示剩余待传输的文件字节长度
        if stat.S_ISREG(statobj.st_mode):
            response['Content-Length'] = statobj.st_size - start_bytes
        if encoding:
            response['Content-Encoding'] = encoding

        # 'Content-Range'的'/'之前描述响应覆盖的文件字节范围，起始下标为0，'/'之后描述整个文件长度，与'HTTP_RANGE'对应使用
        # 参考：http://liqwei.com/network/protocol/2011/886.shtml
        response['Content-Range'] = 'bytes %s-%s/%s' % (start_bytes, statobj.st_size - 1, statobj.st_size)

        # 'Cache-Control'控制浏览器缓存行为，此处禁止浏览器缓存，参考：https://blog.csdn.net/cominglately/article/details/77685214
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response