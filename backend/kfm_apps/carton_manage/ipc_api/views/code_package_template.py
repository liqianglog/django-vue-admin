# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from basics_manage.models import CodePackageTemplate


class IpcCodePackageTemplateSerializer(CustomModelSerializer):
    """
    码包模板管理-序列化器
    """
    package_template_no = serializers.CharField(source="no", read_only=True)

    def to_representation(self,instance):
        result = {
            'package_template_no':instance.no,
            "char_length":instance.char_length,
            "fields":instance.fields,
            "separator":instance.separator,
            "line_feed":instance.line_feed,
            "code_type":instance.code_type
        }
        code_type = instance.code_type
        if code_type==0:
            result["w_url_prefix"]= instance.w_url_prefix
            result["w_url_length"] = instance.w_url_length
            result["w_field_position"] = instance.w_field_position
            return result
        elif code_type==1:
            result["n_url_prefix"] = instance.n_url_prefix
            result["n_url_length"] = instance.n_url_length
            result["n_field_position"] = instance.n_field_position
            return result
        else:
            return super().to_representation(instance=instance)
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


class IpcCodePackageTemplateCreateSerializer(CustomModelSerializer):
    """
    码包模板管理-新增序列化器
    """

    class Meta:
        model = CodePackageTemplate
        fields = "__all__"
        read_only_fields = ["id"]


class IpcCodePackageTemplateUpdateSerializer(CustomModelSerializer):
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
    serializer_class = IpcCodePackageTemplateSerializer
    create_serializer_class = IpcCodePackageTemplateCreateSerializer
    update_serializer_class = IpcCodePackageTemplateUpdateSerializer
    @action(methods=['post'],detail=False,permission_classes=[IsAuthenticated])
    def get_detail(self, request, *args, **kwargs):
        params = request.data
        package_template_no = params.get('package_template_no', None)
        if package_template_no is None:
            return ErrorResponse(msg="未获取到模板编号")
        else:
            queryset =self.get_queryset().filter(no=package_template_no).first()
            if queryset is None:
                return ErrorResponse(msg="模板编号不正确")
            serializer = IpcCodePackageTemplateSerializer(queryset, many=False)
            return DetailResponse(data=serializer.data)
