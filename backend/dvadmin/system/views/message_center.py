# -*- coding: utf-8 -*-
from itertools import chain

from django_restql.fields import DynamicSerializerMethodField
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from dvadmin.system.models import MessageCenter, Users
from dvadmin.system.views.role import RoleSerializer
from dvadmin.system.views.user import UserSerializer
from dvadmin.utils.json_response import SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class MessageCenterSerializer(CustomModelSerializer):
    """
    消息中心-序列化器
    """
    role_info = DynamicSerializerMethodField()
    user_info = DynamicSerializerMethodField()
    def get_role_info(self, instance, parsed_query):
        roles =instance.target_role.all()
        # You can do what ever you want in here
        # `parsed_query` param is passed to BookSerializer to allow further querying
        serializer = RoleSerializer(
            roles,
            many=True,
            parsed_query=parsed_query
        )
        return serializer.data

    def get_user_info(self, instance, parsed_query):
        users = instance.target_user.all()
        # You can do what ever you want in here
        # `parsed_query` param is passed to BookSerializer to allow further querying
        serializer = UserSerializer(
            users,
            many=True,
            parsed_query=parsed_query
        )
        return serializer.data

    class Meta:
        model = MessageCenter
        fields = "__all__"
        read_only_fields = ["id"]


class MessageCenterCreateSerializer(CustomModelSerializer):
    """
    消息中心-新增-序列化器
    """

    def save(self, **kwargs):
        data = super().save(**kwargs)
        initial_data = self.initial_data
        target_type = initial_data.get('target_type')
        # 在保存之前,根据目标类型,把目标用户查询出来并保存
        users = initial_data.get('target_user',[])
        if target_type in [1]:
            target_role = initial_data.get('target_role')
            users = Users.objects.exclude(is_deleted=True).filter(role__id__in=target_role).values_list('id',flat=True)
        if target_type in [2]:
            target_dept = initial_data.get('target_dept')
            users = Users.objects.exclude(is_deleted=True).filter(dept__id__in=target_dept).values_list('id',flat=True)
        data.save()
        data.target_user.set(users)
        return data

    class Meta:
        model = MessageCenter
        fields = "__all__"
        read_only_fields = ["id"]




class MessageCenterViewSet(CustomModelViewSet):
    """
    消息中心接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = MessageCenter.objects.all()
    serializer_class = MessageCenterSerializer
    create_serializer_class = MessageCenterCreateSerializer
    extra_filter_backends = []

    @action(methods=['GET'],detail=False,permission_classes=[IsAuthenticated])
    def get_self_receive(self,request):
        """
        获取接收到的消息
        """
        self_user_id = self.request.user.id
        queryset = MessageCenter.objects.filter(target_user__id=self_user_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg="获取成功")