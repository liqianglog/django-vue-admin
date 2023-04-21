import mimetypes

from rest_framework import serializers

from dvadmin.system.models import FileList
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class FileSerializer(CustomModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    def get_url(self, instance):
        # return 'media/' + str(instance.url)
        return instance.file_url or 'media/' + str(instance.url)

    class Meta:
        model = FileList
        fields = "__all__"

    def create(self, validated_data):
        validated_data['name'] = str(self.initial_data.get('file'))
        # 1. 是否需要备份到本地服务器
        # 2. 需要备份就把 validated_data['url'] 赋值
        validated_data['url'] = self.initial_data.get('file')
        # 3. 上传到云对象存储
        # 4. 如果不需要备份，需要把
        # validated_data['size']
        # validated_data['file_url']
        # validated_data['md5']
        # validated_data['engine']
        # 5. 获取一下媒体类型 mime_type 进行保存
        validated_data['mime_type'] = mimetypes.guess_type(self.initial_data.get('file'))[0]
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
