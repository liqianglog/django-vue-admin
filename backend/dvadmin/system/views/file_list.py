from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser

from dvadmin.system.models import FileList
from dvadmin.utils.json_response import SuccessResponse
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
        print(self.context['request'])
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

    @action(detail=False, methods=['post'])
    def test_post_file(self, request):

        return SuccessResponse(msg='test_is_ok')
