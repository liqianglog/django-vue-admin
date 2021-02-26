from rest_framework import serializers

from apps.op_drf.serializers import CustomModelSerializer
from apps.permission.models import Menu, Dept, Post, Role, UserProfile


# ================================================= #
# ************** 用户管理 序列化器  ************** #
# ================================================= #


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


# ================================================= #
# ************** 菜单管理 序列化器  ************** #
# ================================================= #

class MenuSerializer(CustomModelSerializer):
    """
    简单菜单序列化器
    """
    parentId = serializers.IntegerField(source="parentId.id", default=0)

    class Meta:
        model = Menu
        exclude = ('description', 'creator', 'modifier')


class MenuCreateUpdateSerializer(CustomModelSerializer):
    """
    菜单管理 创建/更新时的列化器
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
        exclude = ('description', 'creator', 'modifier')
        read_only_fields = ('update_datetime', 'create_datetime', 'creator', 'modifier')


class MenuTreeSerializer(serializers.ModelSerializer):
    """
    菜单树形架构序列化器:递归序列化所有深度的子菜单
    """
    label = serializers.CharField(source='name', default='')
    parentId = serializers.IntegerField(source="parentId.id", default=0)

    class Meta:
        model = Menu
        fields = ('id', 'label', 'parentId')


# ================================================= #
# ************** 部门管理 序列化器  ************** #
# ================================================= #

class DeptSerializer(CustomModelSerializer):
    """
    部门管理 简单序列化器
    """
    parentId = serializers.IntegerField(source="parentId.id", default=0)

    class Meta:
        model = Dept
        exclude = ('description', 'creator', 'modifier')


class DeptCreateUpdateSerializer(CustomModelSerializer):
    """
    部门管理 创建/更新时的列化器
    """

    def validate(self, attrs: dict):
        return super().validate(attrs)

    class Meta:
        model = Dept
        exclude = ('description', 'creator', 'modifier')
        read_only_fields = ('update_datetime', 'create_datetime', 'creator', 'modifier')


class DeptTreeSerializer(serializers.ModelSerializer):
    """
    部门树形架构序列化器:递归序列化所有深度的子部门
    """
    label = serializers.CharField(source='deptName', default='')
    parentId = serializers.IntegerField(source="parentId.id", default=0)

    class Meta:
        model = Dept
        fields = ('id', 'label', 'parentId')


# ================================================= #
# ************** 岗位管理 序列化器  ************** #
# ================================================= #

class PostSerializer(CustomModelSerializer):
    """
    岗位管理 简单序列化器
    """

    class Meta:
        model = Post
        exclude = ('description', 'creator', 'modifier')


class PostCreateUpdateSerializer(CustomModelSerializer):
    """
    岗位管理 创建/更新时的列化器
    """

    def validate(self, attrs: dict):
        return super().validate(attrs)

    class Meta:
        model = Post
        exclude = ('description', 'creator', 'modifier')
        read_only_fields = ('update_datetime', 'create_datetime', 'creator', 'modifier')


# ================================================= #
# ************** 角色管理 序列化器  ************** #
# ================================================= #

class RoleSerializer(CustomModelSerializer):
    """
    角色管理 简单序列化器
    """

    class Meta:
        model = Role
        exclude = ('description', 'creator', 'modifier')


class RoleCreateUpdateSerializer(CustomModelSerializer):
    """
    角色管理 创建/更新时的列化器
    """
    menu = MenuSerializer(many=True, read_only=True)
    dept = DeptSerializer(many=True, read_only=True)

    def validate(self, attrs: dict):
        return super().validate(attrs)

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.dept.set(self.initial_data.get('dept'))
        data.menu.set(self.initial_data.get('menu'))
        return data

    class Meta:
        model = Role
        exclude = ('description', 'creator', 'modifier')
        read_only_fields = ('update_datetime', 'create_datetime', 'creator', 'modifier')
