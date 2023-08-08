from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from device.models import Template, TemplateDetail


class TemplateSerializer(CustomModelSerializer):
    """模板管理序列化器"""

    class Meta:
        model = Template
        fields = '__all__'
        read_only_fields = ['id']


class TemplateDetailSerializer(CustomModelSerializer):
    """模板详情序列化器"""

    class Meta:
        model = TemplateDetail
        fields = '__all__'
        read_only_fields = ['id']


class TemplateViewSet(CustomModelViewSet):
    """模板管理视图集"""
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer


class TemplateDetailViewSet(CustomModelViewSet):
    """模板详情视图集"""
    queryset = TemplateDetail.objects.all()
    serializer_class = TemplateDetailSerializer
