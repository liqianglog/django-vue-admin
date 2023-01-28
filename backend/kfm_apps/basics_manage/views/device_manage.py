from rest_framework import serializers

from basics_manage.models import DeviceManage, default_code, default_bind_pwd
from dvadmin.system.models import Users, Role
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class DeviceManageSerializer(CustomModelSerializer):
    """
    生产设备管理-序列化器
    """
    production_line_name = serializers.CharField(source='production_line.name')
    factory_name = serializers.CharField(source='production_line.belong_to_factory.name')
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
