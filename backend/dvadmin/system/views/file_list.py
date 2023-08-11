import base64
import datetime
import hashlib
import json
import os
import random
from pathlib import PurePosixPath

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from rest_framework.decorators import action
from application.settings import BASE_DIR
from application import dispatch, settings
from dvadmin.system.models import FileList, media_file_name
from dvadmin.system.views.ueditor_settings import ueditor_upload_settings, ueditor_settings
from dvadmin.utils.json_response import DetailResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.string_util import format_bytes
from dvadmin.utils.viewset import CustomModelViewSet


class FileSerializer(CustomModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    def get_url(self, instance):
        if self.request.query_params.get('prefix'):
            if settings.ENVIRONMENT in ['local']:
                prefix = 'http://127.0.0.1:8000'
            elif settings.ENVIRONMENT in ['test']:
                prefix = 'http://{host}/api'.format(host=self.request.get_host())
            else:
                prefix = 'https://{host}/api'.format(host=self.request.get_host())
            if instance.file_url:
                return instance.file_url if instance.file_url.startswith('http') else f"{prefix}/{instance.file_url}"
            return (f'{prefix}/media/{str(instance.url)}')
        return instance.file_url or (f'media/{str(instance.url)}')

    class Meta:
        model = FileList
        fields = "__all__"

    def create(self, validated_data):
        file_engine = dispatch.get_system_config_values("file_storage.file_engine") or 'local'
        file_backup = dispatch.get_system_config_values("file_storage.file_backup")
        file = self.initial_data.get('file')
        file_size = file.size
        validated_data['name'] = file.name
        validated_data['size'] = file_size
        md5 = hashlib.md5()
        for chunk in file.chunks():
            md5.update(chunk)
        validated_data['md5sum'] = md5.hexdigest()
        validated_data['engine'] = file_engine
        validated_data['mime_type'] = file.content_type
        if file_backup:
            validated_data['url'] = file
        if file_engine == 'oss':
            from dvadmin_cloud_storage.views.aliyun import ali_oss_upload
            h = validated_data['md5sum']
            basename, ext = os.path.splitext(file.name)
            file_path = ali_oss_upload(file, file_name=PurePosixPath("files", h[:1], h[1:2], h + ext.lower()))
            if file_path:
                validated_data['file_url'] = file_path
            else:
                raise ValueError("上传失败")
        elif file_engine == 'cos':
            from dvadmin_cloud_storage.views.tencent import tencent_cos_upload
            h = validated_data['md5sum']
            basename, ext = os.path.splitext(file.name)
            file_path = tencent_cos_upload(file, file_name=PurePosixPath("files", h[:1], h[1:2], h + ext.lower()))
            if file_path:
                validated_data['file_url'] = file_path
            else:
                raise ValueError("上传失败")
        else:
            validated_data['url'] = file
        # 审计字段
        try:
            request_user = self.request.user
            validated_data['dept_belong_id'] = request_user.dept.id
            validated_data['creator'] = request_user.id
            validated_data['modifier'] = request_user.id
        except:
            pass
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, request=request)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return DetailResponse(data=serializer.data, msg="新增成功")

    @csrf_exempt
    @action(methods=["GET", "POST"], detail=False, permission_classes=[])
    def ueditor(self, request):
        action = self.request.query_params.get("action", "")
        reponse_action = {
            "config": self.get_ueditor_settings,
            "uploadimage": self.upload_file,
            "uploadscrawl": self.upload_file,
            "uploadvideo": self.upload_file,
            "uploadfile": self.upload_file,
        }
        return reponse_action[action](request)

    def get_ueditor_settings(self, request):
        return HttpResponse(json.dumps(ueditor_upload_settings, ensure_ascii=False),
                            content_type="application/javascript")

    # 保存上传的文件
    def save_upload_file(self, file, file_path):
        with open(file_path, 'wb') as f:
            try:
                for chunk in file.chunks():
                    f.write(chunk)

            except Exception as e:
                return f"写入文件错误:{e}"
        return u"SUCCESS"

    def get_path_format_vars(self):
        return {
            "year": datetime.datetime.now().strftime("%Y"),
            "month": datetime.datetime.now().strftime("%m"),
            "day": datetime.datetime.now().strftime("%d"),
            "date": datetime.datetime.now().strftime("%Y%m%d"),
            "time": datetime.datetime.now().strftime("%H%M%S"),
            "datetime": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
            "rnd": random.randrange(100, 999)
        }

    def get_output_path(self, path_format_var):
        """
        取得输出文件的路径
        :param path_format_var:
        :return:
        """
        file_name = (ueditor_settings["defaultPathFormat"] % path_format_var).replace("\\", "/")
        # 分解OutputPathFormat
        output_path = os.path.join('media', 'ueditor', f'{self.request.user.id}')
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        return (file_name, output_path)

    # 涂鸦功能上传处理
    def save_scrawl_file(self, request, file_path, file_name):
        import base64
        instance = None
        try:
            content = request.data.get(ueditor_upload_settings.get("scrawlFieldName", "upfile"))
            f = open(os.path.join(BASE_DIR, file_path, file_name), 'wb')
            f.write(base64.b64decode(content))
            f.close()
            state = "SUCCESS"
            instance = FileList.save_file(request, file_path, file_name, mime_type='image/png')
        except Exception as e:
            state = f"写入图片文件错误:{e}"
        return state, instance

    def upload_file(self, request):
        """上传文件"""
        state = "SUCCESS"
        action = self.request.query_params.get("action")
        # 上传文件
        upload_field_name_list = {
            "uploadfile": "fileFieldName",
            "uploadimage": "imageFieldName",
            "uploadscrawl": "scrawlFieldName",
            "catchimage": "catcherFieldName",
            "uploadvideo": "videoFieldName",
        }
        upload_field_name = self.request.query_params.get(upload_field_name_list[action],
                                                          ueditor_upload_settings.get(action, "upfile"))
        # 上传涂鸦，涂鸦是采用base64编码上传的，需要单独处理
        if action == "uploadscrawl":
            upload_file_name = "scrawl.png"
            upload_file_size = 0
        else:
            # 取得上传的文件
            file = request.FILES.get(upload_field_name, None)
            if file is None:
                return HttpResponse(json.dumps(u"{'state:'ERROR'}"), content_type="application/javascript")
            upload_file_name = file.name
            upload_file_size = file.size

        # 取得上传的文件的原始名称
        upload_original_name, upload_original_ext = os.path.splitext(upload_file_name)
        # 文件类型检验
        upload_allow_type = {
            "uploadfile": "fileAllowFiles",
            "uploadimage": "imageAllowFiles",
            "uploadvideo": "videoAllowFiles"
        }
        if action in upload_allow_type:
            allow_type = list(self.request.query_params.get(upload_allow_type[action],
                                                            ueditor_upload_settings.get(upload_allow_type[action], "")))
            if not upload_original_ext.lower() in allow_type:
                state = u"服务器不允许上传%s类型的文件。" % upload_original_ext
                return HttpResponse({"state": state}, content_type="application/javascript")

        # 大小检验
        upload_max_size = {
            "uploadfile": "filwMaxSize",
            "uploadimage": "imageMaxSize",
            "uploadscrawl": "scrawlMaxSize",
            "uploadvideo": "videoMaxSize"
        }
        max_size = int(self.request.query_params.get(upload_max_size[action],
                                                     ueditor_upload_settings.get(upload_max_size[action], 0)))
        if max_size != 0:
            if upload_file_size > max_size:
                state = u"上传文件大小不允许超过%s。" % format_bytes(max_size)
                return HttpResponse({"state": state}, content_type="application/javascript")

        path_format_var = self.get_path_format_vars()
        path_format_var.update({
            "basename": upload_original_name,
            "extname": upload_original_ext[1:],
            "filename": upload_file_name,
        })
        # 取得输出文件的路径
        format_file_name, output_path = self.get_output_path(path_format_var)
        # 所有检测完成后写入文件
        file_instance = None
        if state == "SUCCESS":
            if action == "uploadscrawl":
                state, file_instance = self.save_scrawl_file(request, file_path=output_path,
                                                             file_name=format_file_name)
            else:
                file = request.FILES.get(upload_field_name, None)
                # 保存到文件中，如果保存错误，需要返回ERROR
                state = self.save_upload_file(file, os.path.join(BASE_DIR, output_path, format_file_name))
                # 保存到附件管理中
                file_instance = FileList.save_file(request, output_path, format_file_name, mime_type=file.content_type)

        # 返回数据
        return_info = {
            'url': file_instance.file_url if file_instance else os.path.join(output_path, format_file_name),  # 保存后的文件名称
            'original': upload_file_name,  # 原始文件名
            'type': upload_original_ext,
            'state': state,  # 上传状态，成功时返回SUCCESS,其他任何值将原样返回至图片上传框中
            'size': upload_file_size
        }
        return HttpResponse(json.dumps(return_info, ensure_ascii=False), content_type="application/javascript")
