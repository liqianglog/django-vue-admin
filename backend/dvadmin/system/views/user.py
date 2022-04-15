# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/6/3 003 0:30
@Remark: 用户管理
"""
import hashlib

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from dvadmin.system.models import Users
from dvadmin.utils.json_response import ErrorResponse, DetailResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.validator import CustomUniqueValidator
from dvadmin.utils.viewset import CustomModelViewSet


class UserSerializer(CustomModelSerializer):
    """
    用户管理-序列化器
    """

    class Meta:
        model = Users
        read_only_fields = ["id"]
        exclude = ['password']
        extra_kwargs = {
            'post': {'required': False},
        }


class UserCreateSerializer(CustomModelSerializer):
    """
    用户新增-序列化器
    """
    username = serializers.CharField(max_length=50,
                                     validators=[CustomUniqueValidator(queryset=Users.objects.all(), message="账号必须唯一")])
    password = serializers.CharField(required=False, default=make_password(
        hashlib.md5('admin123456'.encode(encoding='UTF-8')).hexdigest()))

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.post.set(self.initial_data.get('post', []))
        return data

    class Meta:
        model = Users
        fields = "__all__"
        read_only_fields = ["id"]
        extra_kwargs = {
            'post': {'required': False},
        }


class UserUpdateSerializer(CustomModelSerializer):
    """
    用户修改-序列化器
    """
    username = serializers.CharField(max_length=50,
                                     validators=[CustomUniqueValidator(queryset=Users.objects.all(), message="账号必须唯一")])
    password = serializers.CharField(required=False, allow_blank=True)

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.post.set(self.initial_data.get('post', []))
        return data

    class Meta:
        model = Users
        read_only_fields = ["id"]
        fields = "__all__"
        extra_kwargs = {
            'post': {'required': False, 'read_only': True},
        }


class ExportUserProfileSerializer(CustomModelSerializer):
    """
    用户导出 序列化器
    """
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    dept__deptName = serializers.CharField(source='dept.deptName', default='')
    dept__owner = serializers.CharField(source='dept.owner', default='')
    gender = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = Users
        fields = ('username', 'name', 'email', 'mobile', 'gender', 'is_active', 'last_login', 'dept__deptName',
                  'dept__owner')


class UserProfileImportSerializer(CustomModelSerializer):

    def save(self, **kwargs):
        data = super().save(**kwargs)
        password = hashlib.new('md5', str(self.initial_data.get('password', '')).encode(encoding='UTF-8')).hexdigest()
        data.set_password(password)
        data.save()
        return data

    def run_validation(self, data={}):
        # 把excel 数据进行格式转换
        if type(data) is dict:
            data['role'] = str(data['role']).split(',')
            data['dept_id'] = str(data['dept']).split(',')
            data['gender'] = {'男': '1', '女': '0', '未知': '2'}.get(data['gender'])
            data['is_active'] = {'启用': True, '禁用': False}.get(data['is_active'])
        return super().run_validation(data)

    class Meta:
        model = Users
        exclude = ('password', 'post', 'user_permissions', 'groups', 'is_superuser', 'date_joined')


class UserViewSet(CustomModelViewSet):
    """
    用户接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Users.objects.exclude(is_superuser=1).all()
    serializer_class = UserSerializer
    create_serializer_class = UserCreateSerializer
    update_serializer_class = UserUpdateSerializer
    filter_fields = ['name', 'username', 'gender', 'is_active', 'dept', 'user_type']
    # filter_fields = {
    #     'name': ['icontains'],
    #     'username': ['icontains'],
    #     'gender': ['icontains'],
    #     'is_active': ['icontains'],
    #     'dept': ['exact'],
    # }
    search_fields = ['username', 'name', 'gender', 'dept__name', 'role__name']
    # 导出
    export_field_label = ['用户账号', '用户名称', '用户邮箱', '手机号码', '用户性别', '帐号状态', '最后登录时间', '部门名称', '部门负责人']
    export_serializer_class = ExportUserProfileSerializer
    # 导入
    import_serializer_class = UserProfileImportSerializer
    import_field_dict = {'username': '登录账号', 'name': '用户名称', 'email': '用户邮箱', 'mobile': '手机号码',
                         'gender': '用户性别(男/女/未知)',
                         'is_active': '帐号状态(启用/禁用)', 'password': '登录密码', 'dept': '部门ID', 'role': '角色ID'}

    @action(methods=['GET'], detail=True, permission_classes=[IsAuthenticated])
    def user_info(self, request):
        """获取当前用户信息"""
        user = request.user
        result = {
            "name": user.name,
            "mobile": user.mobile,
            "gender": user.gender,
            "email": user.email
        }
        return DetailResponse(data=result, msg="获取成功")

    @action(methods=['PUT'], detail=True, permission_classes=[IsAuthenticated])
    def update_user_info(self, request):
        """修改当前用户信息"""
        user = request.user
        Users.objects.filter(id=user.id).update(**request.data)
        return DetailResponse(data=None, msg="修改成功")

    @action(methods=['PUT'], detail=True, permission_classes=[IsAuthenticated])
    def change_password(self, request, *args, **kwargs):
        """密码修改"""
        instance = Users.objects.filter(id=kwargs.get('pk')).first()
        data = request.data
        old_pwd = data.get('oldPassword')
        new_pwd = data.get('newPassword')
        new_pwd2 = data.get('newPassword2')
        if instance:
            if new_pwd != new_pwd2:
                return ErrorResponse(msg="两次密码不匹配")
            elif instance.check_password(old_pwd):
                instance.password = make_password(new_pwd)
                instance.save()
                return DetailResponse(data=None, msg="修改成功")
            else:
                return ErrorResponse(msg="旧密码不正确")
        else:
            return ErrorResponse(msg="未获取到用户")

    @action(methods=['PUT'], detail=True)
    def reset_password(self, request, pk):
        """
        密码重置
        """
        instance = Users.objects.filter(id=pk).first()
        data = request.data
        new_pwd = data.get('newPassword')
        new_pwd2 = data.get('newPassword2')
        if instance:
            if new_pwd != new_pwd2:
                return ErrorResponse(msg="两次密码不匹配")
            else:
                instance.password = make_password(new_pwd)
                instance.save()
                return DetailResponse(data=None, msg="修改成功")
        else:
            return ErrorResponse(msg="未获取到用户")
