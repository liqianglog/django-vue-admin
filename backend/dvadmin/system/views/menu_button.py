# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/6/3 003 0:30
@Remark: 菜单按钮管理
"""
from django.db.models import F, CharField, Value, ExpressionWrapper
from django.db.models.functions import Cast, Concat
from rest_framework.decorators import action

from dvadmin.system.models import MenuButton, Menu
from dvadmin.utils.json_response import DetailResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class MenuButtonSerializer(CustomModelSerializer):
    """
    菜单按钮-序列化器
    """

    class Meta:
        model = MenuButton
        fields = ["id", "name", "value", "api", "method", "menu"]
        read_only_fields = ["id"]


class MenuButtonInitSerializer(CustomModelSerializer):
    """
    初始化菜单按钮-序列化器
    """

    class Meta:
        model = MenuButton
        fields = ["id", "name", "value", "api", "method", "menu"]
        read_only_fields = ["id"]


class MenuButtonCreateUpdateSerializer(CustomModelSerializer):
    """
    初始化菜单按钮-序列化器
    """

    class Meta:
        model = MenuButton
        fields = "__all__"
        read_only_fields = ["id"]


class MenuButtonViewSet(CustomModelViewSet):
    """
    菜单按钮接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = MenuButton.objects.all()
    serializer_class = MenuButtonSerializer
    create_serializer_class = MenuButtonCreateUpdateSerializer
    update_serializer_class = MenuButtonCreateUpdateSerializer
    extra_filter_backends = []

    @action(methods=["GET"], detail=False, permission_classes=[])
    def get_btn_permission(self, request):
        """
        获取当前用户的按钮权限
        """
        user = request.user
        if not user.is_superuser:
            menuIds = user.role.values_list("menu__id", flat=True)
        else:
            menuIds = Menu.objects.filter(status=1)
        queryset = (
            MenuButton.objects.filter(menu__in=menuIds)
            .annotate(permission=Concat("menu__web_path", Value(":"), "value", output_field=CharField()))
            .values_list("permission", flat=True)
        )
        return DetailResponse(data=queryset)
