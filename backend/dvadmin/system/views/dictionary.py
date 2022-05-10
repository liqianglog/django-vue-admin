# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/6/3 003 0:30
@Remark: 字典管理
"""
from dvadmin.system.models import Dictionary
from dvadmin.utils.json_response import SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from rest_framework import serializers


class DictionarySerializer(CustomModelSerializer):
    """
    字典-序列化器
    """

    class Meta:
        model = Dictionary
        fields = "__all__"
        read_only_fields = ["id"]


class DictionaryCreateUpdateSerializer(CustomModelSerializer):
    """
    字典管理 创建/更新时的列化器
    """

    class Meta:
        model = Dictionary
        fields = '__all__'


class DictionaryTreeSerializer(CustomModelSerializer):
    """
    字典表的树形序列化器
    """
    children = serializers.SerializerMethodField(read_only=True)

    def get_children(self, instance):
        queryset = Dictionary.objects.filter(parent=instance.id).filter(status=1).values('label', 'value', 'type')
        if queryset:
            return queryset
        else:
            return []

    class Meta:
        model = Dictionary
        fields = ['id', 'value', 'children']
        read_only_fields = ["id"]


class DictionaryViewSet(CustomModelViewSet):
    """
    字典管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Dictionary.objects.all()
    serializer_class = DictionarySerializer
    extra_filter_backends = []
    search_fields = ['label']

    def list(self, request, *args, **kwargs):
        dictionary_key = self.request.query_params.get('dictionary_key')
        if dictionary_key:
            if dictionary_key == 'all':
                queryset = self.queryset.filter(status=True, is_value=False)
                serializer = DictionaryTreeSerializer(queryset, many=True, request=request)
                data = serializer.data
            else:
                data = self.queryset.filter(parent__value=dictionary_key, status=True).values('label', 'value', 'type')
            return SuccessResponse(data=data, msg="获取成功")
        return super().list(request, *args, **kwargs)
