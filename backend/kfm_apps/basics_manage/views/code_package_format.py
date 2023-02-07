from basics_manage.models import CodePackageFormat
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class CodePackageFormatSerializer(CustomModelSerializer):
    """
   码包回传格式-序列化器
    """

    class Meta:
        model = CodePackageFormat
        fields = "__all__"
        read_only_fields = ["id"]


class CodePackageFormatCreateUpdateSerializer(CustomModelSerializer):
    """
   码包回传格式管理 创建/更新时的列化器
    """

    class Meta:
        model = CodePackageFormat
        fields = '__all__'


class CodePackageFormatViewSet(CustomModelViewSet):
    """
   码包回传格式管理接口:
    """
    queryset = CodePackageFormat.objects.all()
    serializer_class = CodePackageFormatSerializer
    create_serializer_class = CodePackageFormatCreateUpdateSerializer
    update_serializer_class = CodePackageFormatCreateUpdateSerializer
    search_fields = ['no']
