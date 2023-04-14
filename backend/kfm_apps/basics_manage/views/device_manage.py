from urllib.parse import urlsplit

from django.contrib.auth.models import update_last_login
from django.db import connection
from django_tenants.utils import schema_context
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from application import settings
from application.settings import APP_ACCESS_TOKEN_LIFETIME
from basics_manage.models import DeviceManage, default_code, default_bind_pwd
from dvadmin.system.models import Users, Role
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin_tenants.models import Client, Domain


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.clear()
        self.fields['device_code'] = serializers.CharField()
        self.fields['device_pwd'] = serializers.CharField()

    @classmethod
    def get_token(cls, user):
        Refresh = AccessToken
        Refresh.lifetime = APP_ACCESS_TOKEN_LIFETIME
        token = Refresh.for_user(user)
        # Add custom claims
        token['production_line_id'] = user.production_line_id
        token['device_id'] = user.device_id
        return token

    def validate(self, attrs):
        # 获取所有租户名
        if connection.tenant.schema_name == "public":
            schema_name_list = Client.objects.exclude(schema_name="public").values_list('schema_name', flat=True)
        else:
            schema_name_list = [connection.tenant.schema_name]
        _DeviceManage = None
        data = {}
        _schema_name = None
        # 通过设备编号从所有租户中获取设备
        for schema_name in schema_name_list:
            with schema_context(schema_name):
                _DeviceManage = DeviceManage.objects.filter(no=attrs.get('device_code')).first()
                if _DeviceManage:
                    _schema_name = schema_name
                    domain_obj = Domain.objects.filter(is_primary=True, tenant__schema_name=schema_name).first()
                    request = self.context.get('request')
                    http = urlsplit(request.build_absolute_uri(None)).scheme
                    if settings.ENVIRONMENT == "prod":
                        data['domain'] = f"https://{domain_obj.domain}/api"
                    elif settings.ENVIRONMENT == "test":
                        data['domain'] = f"http://{domain_obj.domain}/api"
                    else:
                        data['domain'] = f"{http}://{domain_obj.domain}:{request.META['SERVER_PORT']}/api"
                    break
        if not _schema_name:
            raise exceptions.AuthenticationFailed("设备编号或密码错误", )
        with schema_context(_schema_name):
            if not (_DeviceManage and _DeviceManage.password == attrs.get('device_pwd')):
                raise exceptions.AuthenticationFailed("设备编号或密码错误!", )
            if not (_DeviceManage and _DeviceManage.user):
                raise exceptions.AuthenticationFailed("此设备未关联用户!", )
            if not _DeviceManage.production_line_id:
                raise exceptions.AuthenticationFailed("此设备未关联产线!", )
            self.user = _DeviceManage.user
            self.user.production_line_id = _DeviceManage.production_line_id
            self.user.device_id = _DeviceManage.id
            if not api_settings.USER_AUTHENTICATION_RULE(self.user):
                raise exceptions.AuthenticationFailed("用户未激活，请联系管理员!")
            refresh = self.get_token(self.user)
            data['token'] = str(refresh)
            # data['token'] = str(refresh.access_token)
            if api_settings.UPDATE_LAST_LOGIN:
                update_last_login(None, self.user)
            return {
                "code": 2000,
                "data": data,
                "msg": "登录成功"
            }


class DeviceManageLogin(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class DeviceManageSerializer(CustomModelSerializer):
    """
    生产设备管理-序列化器
    """
    production_line_name = serializers.CharField(source='production_line.name',read_only=True)
    factory_name = serializers.CharField(source='production_line.belong_to_factory.name',read_only=True)
    factory_id = serializers.CharField(source='production_line.belong_to_factory.id', read_only=True)

    class Meta:
        model = DeviceManage
        fields = "__all__"
        read_only_fields = ["id"]


class DeviceManageCreateSerializer(CustomModelSerializer):
    """
    设备管理-新增序列化器
    """

    class Meta:
        model = DeviceManage
        fields = "__all__"
        read_only_fields = ["id"]

    def create(self, validated_data):
        no = default_code()
        password = default_bind_pwd()
        validated_data['no'] = no
        validated_data['password'] = password
        name = "[device]" + no
        user = Users.objects.create(username=no, password="", is_active=True, name=name, user_type=2,
                                    dept_id=self.request.user.dept_id or None)
        role_obj = Role.objects.filter(key='device_manage').first()
        if role_obj:
            user.role.set([role_obj.id])
        validated_data['user'] = user
        return super().create(validated_data)


class DeviceManageUpdateSerializer(CustomModelSerializer):
    """
    生产设备管理 创建/更新时的列化器
    """

    class Meta:
        model = DeviceManage
        fields = '__all__'


class DeviceManageViewSet(CustomModelViewSet):
    """
    生产设备管理接口:
    """
    queryset = DeviceManage.objects.all()
    serializer_class = DeviceManageSerializer
    create_serializer_class = DeviceManageCreateSerializer
    update_serializer_class = DeviceManageUpdateSerializer
    search_fields = ['no', 'name']
