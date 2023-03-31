# -*- coding: utf-8 -*-


from django.db.models import F
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from dvadmin.system.models import RoleMenuPermission, Menu, MenuButton
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class RoleMenuPermissionSerializer(CustomModelSerializer):
    """
    菜单按钮-序列化器
    """

    class Meta:
        model = RoleMenuPermission
        fields = "__all__"
        read_only_fields = ["id"]


class RoleMenuPermissionInitSerializer(CustomModelSerializer):
    """
    初始化菜单按钮-序列化器
    """

    class Meta:
        model = RoleMenuPermission
        fields = "__all__"
        read_only_fields = ["id"]

class RoleMenuPermissionCreateUpdateSerializer(CustomModelSerializer):
    """
    初始化菜单按钮-序列化器
    """

    class Meta:
        model = RoleMenuPermission
        fields = "__all__"
        read_only_fields = ["id"]


class RoleMenuPermissionViewSet(CustomModelViewSet):
    """
    菜单按钮接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = RoleMenuPermission.objects.all()
    serializer_class = RoleMenuPermissionSerializer
    create_serializer_class = RoleMenuPermissionCreateUpdateSerializer
    update_serializer_class = RoleMenuPermissionCreateUpdateSerializer
    extra_filter_class = []

    @action(methods=['post'],detail=False)
    def save_auth(self,request):
        """
        保存页面菜单授权
        :param request:
        :return:
        """
        body = request.data
        role_id = body.get('role',None)
        if role_id is None:
            return ErrorResponse(msg="未获取到角色参数")
        menu_list = body.get('menu',None)
        if menu_list is None:
            return ErrorResponse(msg="未获取到菜单参数")
        data = [{"role":role_id,"menu":item} for item in menu_list]
        serializer = RoleMenuPermissionSerializer(data=data,many=True,request=request)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return DetailResponse(msg="保存成功",data=serializer.data)
