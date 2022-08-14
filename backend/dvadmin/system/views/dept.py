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
    status_label = serializers.SerializerMethodField()

    def get_has_children(self, obj: Dept):
        return Dept.objects.filter(parent_id=obj.id).count()

    def get_status_label(self, instance):
        status = instance.status
        if status:
            return "启用"
        return "禁用"

    class Meta:
        model = Dept
        fields = '__all__'
        read_only_fields = ["id"]


class DeptInitSerializer(CustomModelSerializer):
    """
    递归深度获取数信息(用于生成初始化json文件)
    """
    children = serializers.SerializerMethodField()

    def get_children(self, obj: Dept):
        data = []
        instance = Dept.objects.filter(parent_id=obj.id)
        if instance:
            serializer = DeptInitSerializer(instance=instance, many=True)
            data = serializer.data
        return data

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        children = self.initial_data.get('children')
        if children:
            for menu_data in children:
                menu_data['parent'] = instance.id
                filter_data = {
                    "name": menu_data['name'],
                    "parent": menu_data['parent']
                }
                instance_obj = Dept.objects.filter(**filter_data).first()
                if instance_obj and not self.initial_data.get('reset'):
                    continue
                serializer = DeptInitSerializer(instance_obj, data=menu_data, request=self.request)
                serializer.is_valid(raise_exception=True)
                serializer.save()

        return instance

    class Meta:
        model = Dept
        fields = ['name', 'sort', 'owner', 'phone', 'email', 'status', 'parent', 'creator', 'dept_belong_id',
                  'children']
        extra_kwargs = {
            'creator': {'write_only': True},
            'dept_belong_id': {'write_only': True}
        }
        read_only_fields = ['id', 'children']


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
                if self.request.user.is_superuser:
                    queryset = queryset.filter(parent__isnull=True)
                else:
                    queryset = queryset.filter(id=self.request.user.dept_id)
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
            if self.request.user.is_superuser:
                queryset = queryset.filter(parent__isnull=True)
            else:
                queryset = queryset.filter(id=self.request.user.dept_id)
        data = queryset.filter(status=True).order_by('sort').values('name', 'id', 'parent')
        return DetailResponse(data=data, msg="获取成功")
