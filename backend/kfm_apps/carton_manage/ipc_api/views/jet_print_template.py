# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from basics_manage.models import JetPrintTemplate
from utils.permission import DeviceManagePermission


class IpcJetPrintTemplateSerializer(CustomModelSerializer):
    """
    喷码模板管理-序列化器
    """
    def to_representation(self, instance):
        result = {
            'no': instance.no,
            'name':instance.name,
            "fields": instance.fields,
            "carton_number": instance.carton_number,
            "img": instance.img,
            "update_datetime":instance.update_datetime.strftime("%Y-%m-%d %H:%M:%S" ),
            "code_package_template_no": instance.code_package_template.no,
            "attribute": instance.jetprinttemplateattribute_set.values('number','name','line_number','column_number').order_by('number')
        }
        return result


    class Meta:
        model = JetPrintTemplate
        fields = [
            'no',
            "name",
            "fields",
            "carton_number",
            "img",
            "attribute"
        ]
        read_only_fields = ["id"]


class IpcJetPrintTemplateCreateSerializer(CustomModelSerializer):
    """
    喷码模板管理-新增序列化器
    """

    class Meta:
        model = JetPrintTemplate
        fields = "__all__"
        read_only_fields = ["id"]


class IpcJetPrintTemplateUpdateSerializer(CustomModelSerializer):
    """
    喷码模板管理-更新列化器
    """

    class Meta:
        model = JetPrintTemplate
        fields = '__all__'


class JetPrintTemplateViewSet(CustomModelViewSet):
    """
    喷码模板管理接口:
    """
    queryset = JetPrintTemplate.objects.all()
    serializer_class = IpcJetPrintTemplateSerializer
    create_serializer_class = IpcJetPrintTemplateCreateSerializer
    update_serializer_class = IpcJetPrintTemplateUpdateSerializer
    permission_classes = [DeviceManagePermission]
    extra_filter_backends = []

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def get_detail(self, request, *args, **kwargs):
        params = request.data
        jet_print_template_no = params.get('jet_print_template_no', None)
        if jet_print_template_no is None:
            return ErrorResponse(msg="未获取到模板编号")
        else:
            queryset = self.get_queryset().filter(no=jet_print_template_no).first()
            if queryset is None:
                return ErrorResponse(msg="模板编号不正确")
            serializer = IpcJetPrintTemplateSerializer(queryset, many=False)
            return DetailResponse(data=serializer.data)
