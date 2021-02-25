from rest_framework import serializers

from apps.op_drf.serializers import CustomModelSerializer
from apps.permission.models import UserProfile, Menu, Role


class UserProfileSerializer(CustomModelSerializer):
    """
    简单用户序列化器
    """
    admin = serializers.SerializerMethodField(read_only=True)

    def get_admin(self, obj: UserProfile):
        role_list = obj.role.all().values_list('admin', flat=True)
        if True in list(set(role_list)):
            return True
        return False

    class Meta:
        model = UserProfile
        dept = 2
        exclude = ('password', 'secret', 'user_permissions', 'groups', 'is_superuser', 'date_joined')


class MenuSerializer(CustomModelSerializer):
    """
    简单菜单序列化器
    """
    parentId = serializers.IntegerField(source="parentId.id", default=0)
    class Meta:
        model = Menu
        fields = '__all__'


class CreateUpdateMenuSerializer(CustomModelSerializer):
    """
    创建角色/更新时的列化器
    """

    def validate(self, attrs: dict):
        # name = attrs['name']
        # role: Role = Role.objects.filter(name=name).first()
        # if role and attrs.get('instanceId', '') != role.instanceId:
        #     raise APIException(message=f'角色名称[{name}]不能重复')
        # if getattr(self.instance, 'is_public', False) or attrs.get('is_public', False):
        #     up = UserPermission(self.request.user)
        #     if not up.is_manager():
        #         raise APIException(message=f'仅Manger能创建/更新角色为公共角色')
        return super().validate(attrs)

    class Meta:
        model = Menu
        fields = "__all__"
        read_only_fields = ('mtime', 'ctime', 'creator', 'modifier')


class RoleSerializer(serializers.ModelSerializer):
    """
    简单角色序列化器
    """

    class Meta:
        model = Role
        fields = '__all__'
