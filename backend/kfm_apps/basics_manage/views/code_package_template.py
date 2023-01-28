from basics_manage.models import CodePackageTemplate
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class CodePackageTemplateSerializer(CustomModelSerializer):
    """
    码包模板-序列化器
    """

    class Meta:
        model = CodePackageTemplate
        fields = "__all__"
        read_only_fields = ["id"]


class CodePackageTemplateCreateUpdateSerializer(CustomModelSerializer):
    """
    码包模板管理 创建/更新时的列化器
    """

    class Meta:
        model = CodePackageTemplate
        fields = '__all__'


class CodePackageTemplateViewSet(CustomModelViewSet):
    """
    码包模板管理接口:
    """
    queryset = CodePackageTemplate.objects.all()
    serializer_class = CodePackageTemplateSerializer
    create_serializer_class = CodePackageTemplateCreateUpdateSerializer
    update_serializer_class = CodePackageTemplateCreateUpdateSerializer
    search_fields = ['no', 'name', 'w_url_prefix', 'n_url_prefix']
