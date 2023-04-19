# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from basics_manage.models import CodePackageTemplate
from utils.permission import DeviceManagePermission


class IpcCodePackageTemplateSerializer(CustomModelSerializer):
    """
    码包模板管理-序列化器
    """
    def to_representation(self, instance):
        result = {
            'no': instance.no,
            'name':instance.name,
            "char_length": instance.char_length,
            "fields": instance.fields,
            "separator": instance.separator,
            "line_feed": instance.line_feed,
            "attribute": instance.codepackagetemplateattribute_set.values('number','name','char_length','verify_matches','is_code_content').order_by('number')
        }
        return result


    class Meta:
        model = CodePackageTemplate
        fields = [
            'no',
            "char_length",
            "fields",
            "separator",
            "line_feed",
            'name',
            'attribute'
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
    permission_classes = [DeviceManagePermission]
    extra_filter_backends = []

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def get_detail(self, request, *args, **kwargs):
        params = request.data
        package_template_no = params.get('package_template_no', None)
        if package_template_no is None:
            return ErrorResponse(msg="未获取到模板编号")
        else:
            queryset = self.get_queryset().filter(no=package_template_no).first()
            if queryset is None:
                return ErrorResponse(msg="模板编号不正确")
            serializer = IpcCodePackageTemplateSerializer(queryset, many=False)
            return DetailResponse(data=serializer.data)
