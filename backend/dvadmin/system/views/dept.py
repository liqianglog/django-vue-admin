# -*- coding: utf-8 -*-

"""
@author: H0nGzA1
@contact: QQ:2505811377
@Remark: 部门管理
"""
from rest_framework import serializers

from dvadmin.system.models import Dept
from dvadmin.utils.json_response import DetailResponse, SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class DeptSerializer(CustomModelSerializer):
    """
    部门-序列化器
    """
    parent_name = serializers.CharField(read_only=True, source='parent.name')
    has_children = serializers.SerializerMethodField()

    def get_has_children(self, obj: Dept):
        return Dept.objects.filter(parent_id=obj.id).count()

    class Meta:
        model = Dept
        fields = '__all__'
        read_only_fields = ["id"]


class DeptQuerySerializer(CustomModelSerializer):
    """
    部门-序列化器
    """
    parent_name = serializers.CharField(read_only=True, source='parent.name')
    code = serializers.CharField(source='id')

    class Meta:
        model = Dept
        fields = ['id', 'name', 'parent', 'parent_name', 'code']
        read_only_fields = ["id"]


class DeptCreateUpdateSerializer(CustomModelSerializer):
    """
    部门管理 创建/更新时的列化器
    """

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.dept_belong_id = instance.id
        instance.save()
        return instance

    class Meta:
        model = Dept
        fields = '__all__'


class DeptViewSet(CustomModelViewSet):
    """
    部门管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Dept.objects.all()
    serializer_class = DeptSerializer
    create_serializer_class = DeptCreateUpdateSerializer
    update_serializer_class = DeptCreateUpdateSerializer
    filter_fields = ['name', 'id', 'parent']
    search_fields = []

    # extra_filter_backends = []

    def list(self, request, *args, **kwargs):
        # 如果懒加载，则只返回父级
        queryset = self.filter_queryset(self.get_queryset())
        lazy = self.request.query_params.get('lazy')
        parent = self.request.query_params.get('parent')
        if lazy:
            # 如果懒加载模式，返回全部
            if not parent:
                queryset = self.queryset.filter(parent__isnull=True)
            serializer = self.get_serializer(queryset, many=True, request=request)
            return SuccessResponse(data=serializer.data, msg="获取成功")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg="获取成功")

    def dept_lazy_tree(self, request, *args, **kwargs):
        parent = self.request.query_params.get('parent')
        queryset = self.filter_queryset(self.get_queryset())
        if not parent:
            queryset = queryset.filter(parent__isnull=True)
        data = queryset.filter(status=True).order_by('sort').values('name', 'id', 'parent')
        return DetailResponse(data=data, msg="获取成功")
