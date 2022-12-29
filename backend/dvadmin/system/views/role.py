# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/6/3 003 0:30
@Remark: 角色管理
"""
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from dvadmin.system.models import Role, Menu
from dvadmin.system.views.dept import DeptSerializer
from dvadmin.system.views.menu import MenuSerializer
from dvadmin.system.views.menu_button import MenuButtonSerializer
from dvadmin.utils.json_response import SuccessResponse, DetailResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.validator import CustomUniqueValidator
from dvadmin.utils.viewset import CustomModelViewSet


class RoleSerializer(CustomModelSerializer):
    """
    角色-序列化器
    """

    class Meta:
        model = Role
        fields = "__all__"
        read_only_fields = ["id"]


class RoleInitSerializer(CustomModelSerializer):
    """
    初始化获取数信息(用于生成初始化json文件)
    """

    class Meta:
        model = Role
        fields = ['name', 'key', 'sort', 'status', 'admin', 'data_range', 'remark',
                  'creator', 'dept_belong_id']
        read_only_fields = ["id"]
        extra_kwargs = {
            'creator': {'write_only': True},
            'dept_belong_id': {'write_only': True}
        }


class RoleCreateUpdateSerializer(CustomModelSerializer):
    """
    角色管理 创建/更新时的列化器
    """
    menu = MenuSerializer(many=True, read_only=True)
    dept = DeptSerializer(many=True, read_only=True)
    permission = MenuButtonSerializer(many=True, read_only=True)
    key = serializers.CharField(max_length=50,
                                validators=[CustomUniqueValidator(queryset=Role.objects.all(), message="权限字符必须唯一")])
    name = serializers.CharField(max_length=50, validators=[CustomUniqueValidator(queryset=Role.objects.all())])

    def validate(self, attrs: dict):
        return super().validate(attrs)

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.dept.set(self.initial_data.get('dept', []))
        data.menu.set(self.initial_data.get('menu', []))
        data.permission.set(self.initial_data.get('permission', []))
        return data

    class Meta:
        model = Role
        fields = '__all__'


class MenuPermissonSerializer(CustomModelSerializer):
    """
    菜单的按钮权限
    """
    menuPermission = MenuButtonSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = '__all__'


class RoleViewSet(CustomModelViewSet):
    """
    角色管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    create_serializer_class = RoleCreateUpdateSerializer
    update_serializer_class = RoleCreateUpdateSerializer
    search_fields = ['name','key']

    @action(methods=['GET'], detail=True, permission_classes=[IsAuthenticated])
    def roleId_get_menu(self, request,pk):
        """通过角色id获取该角色用于的菜单"""
        instance = Role.objects.filter(id=pk).first()
        queryset = instance.menu.all()
        # queryset = Menu.objects.filter(status=1).all()
        queryset = self.filter_queryset(queryset)
        serializer = MenuPermissonSerializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated])
    def data_scope(self,request):
        is_superuser = request.user.is_superuser
        is_admin = Role.objects.filter(users__id=request.user.id,admin=True)
        if is_superuser or is_admin:
            data = [
            {
              "value": 0,
              "label": '仅本人数据权限'
            },
            {
              "value": 1,
              "label": '本部门及以下数据权限'
            },
            {
              "value": 2,
              "label": '本部门数据权限'
            },
            {
              "value": 3,
              "label": '全部数据权限'
            },
            {
              "value": 4,
              "label": '自定义数据权限'
            }
          ]
        else:
            data = [
                {
                    "value": 0,
                    "label": '仅本人数据权限'
                },
                {
                    "value": 1,
                    "label": '本部门及以下数据权限'
                },
                {
                    "value": 2,
                    "label": '本部门数据权限'
                }
            ]
        return DetailResponse(data=data)
