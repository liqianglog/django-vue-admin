# -*- coding: utf-8 -*-
from rest_framework import serializers

from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from kfm_apps.basics_manage.models import CodePackageTemplate


class CodePackageTemplateSerializer(CustomModelSerializer):
    """
    码包模板管理-序列化器
    """
    package_template_no = serializers.CharField(source="no", read_only=True)

    # def to_representation(self,obj):
    #     pass
    class Meta:
        model = CodePackageTemplate
        fields = [
            'package_template_no',
            "char_length",
            "fields",
            "separator",
            "line_feed",
            "code_type",
            "w_url_prefix",
            "w_url_length",
            "w_field_position",
            "n_url_prefix",
            "n_url_length",
            "n_field_position",
        ]
        read_only_fields = ["id"]


class CodePackageTemplateCreateSerializer(CustomModelSerializer):
    """
    码包模板管理-新增序列化器
    """

    class Meta:
        model = CodePackageTemplate
        fields = "__all__"
        read_only_fields = ["id"]


class CodePackageTemplateUpdateSerializer(CustomModelSerializer):
    """
    码包模板管理-更新列化器
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
    create_serializer_class = CodePackageTemplateCreateSerializer
    update_serializer_class = CodePackageTemplateUpdateSerializer

    def list(self, request, *args, **kwargs):
        params = request.query_params
        package_template_no = params.get('package_template_no', None)
        if package_template_no is None:
            return ErrorResponse(msg="未获取到模板编号")
        else:
            queryset = self.filter_queryset(self.get_queryset()).first()
            serializer = CodePackageTemplateSerializer(queryset, many=False)
            return DetailResponse(data=serializer.data)
