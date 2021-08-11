import hashlib

from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.vadmin.op_drf.serializers import CustomModelSerializer
from apps.vadmin.op_drf.validator import CustomUniqueValidator
from apps.vadmin.permission.models import Menu, Dept, Post, Role
from apps.vadmin.system.models import MessagePush

UserProfile = get_user_model()


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

    def save(self, **kwargs):
        Menu.delete_cache()
        return super().save(**kwargs)

    class Meta:
        model = Menu
        fields = '__all__'


class MenuTreeSerializer(serializers.ModelSerializer):
    """
    菜单树形架构序列化器:递归序列化所有深度的子菜单
    """
    label = serializers.CharField(source='name', default='')
    parentId = serializers.IntegerField(source="parentId.id", default=0)

    class Meta:
        model = Menu
        fields = ('id', 'label', 'orderNum', 'parentId')


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
        fields = '__all__'


class DeptTreeSerializer(serializers.ModelSerializer):
    """
    部门树形架构序列化器:递归序列化所有深度的子部门
    """
    label = serializers.CharField(source='deptName', default='')
    parentId = serializers.IntegerField(source="parentId.id", default=0)

    class Meta:
        model = Dept
        fields = ('id', 'label', 'parentId', 'status')


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


class ExportPostSerializer(CustomModelSerializer):
    """
    导出 岗位管理 简单序列化器
    """

    class Meta:
        model = Post
        fields = ('id', 'postName', 'postCode', 'postSort', 'status', 'creator', 'modifier', 'remark')


class PostSimpleSerializer(CustomModelSerializer):
    """
    岗位管理 极简单序列化器
    """

    class Meta:
        model = Post
        fields = ('id', 'postName', 'postCode', 'status')


class PostCreateUpdateSerializer(CustomModelSerializer):
    """
    岗位管理 创建/更新时的列化器
    """

    def validate(self, attrs: dict):
        return super().validate(attrs)

    class Meta:
        model = Post
        fields = '__all__'


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


class ExportRoleSerializer(CustomModelSerializer):
    """
    导出 角色管理 简单序列化器
    """
    dataScope = serializers.SerializerMethodField()

    def get_dataScope(self, obj):
        dataScope = obj.get_dataScope_display()
        return dataScope

    class Meta:
        model = Role
        fields = ('id', 'roleName', 'roleKey', 'roleSort', 'dataScope', 'status', 'creator', 'modifier', 'remark')


class RoleSimpleSerializer(CustomModelSerializer):
    """
    角色管理 极简单序列化器
    """

    class Meta:
        model = Role
        fields = ('id', 'roleName', 'roleKey', 'status')


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
        fields = '__all__'


# ================================================= #
# ************** 用户管理 序列化器  ************** #
# ================================================= #


class UserProfileSerializer(CustomModelSerializer):
    """
    简单用户序列化器
    """
    admin = serializers.SerializerMethodField(read_only=True)
    deptId = serializers.IntegerField(source='dept.id', read_only=True)
    # 未读通知数量
    unread_msg_count = serializers.SerializerMethodField(read_only=True)

    def get_admin(self, obj: UserProfile):
        role_list = obj.role.filter(status='1').values_list('admin', flat=True)
        if True in list(set(role_list)):
            return True
        return False

    def get_unread_msg_count(self, obj: UserProfile):
        return MessagePush.objects.filter(status='2').exclude(messagepushuser_message_push__is_read=True,
                                                              messagepushuser_message_push__user=obj).count()

    class Meta:
        model = UserProfile
        depth = 1
        exclude = ('password', 'secret', 'user_permissions', 'groups', 'is_superuser', 'date_joined', 'creator')


class ExportUserProfileSerializer(CustomModelSerializer):
    """
    用户导出 序列化器
    """
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    dept__deptName = serializers.CharField(source='dept.deptName', default='')
    dept__owner = serializers.CharField(source='dept.owner', default='')

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'name', 'email', 'mobile', 'gender', 'is_active', 'last_login', 'dept__deptName',
                  'dept__owner')


class UserProfileCreateUpdateSerializer(CustomModelSerializer):
    """
    用户管理 创建/更新时的列化器
    """
    admin = serializers.SerializerMethodField(read_only=True)
    post = PostSerializer(many=True, read_only=True)
    role = RoleSerializer(many=True, read_only=True)
    username = serializers.CharField(required=True, max_length=150,
                                     validators=[
                                         CustomUniqueValidator(queryset=UserProfile.objects.all(), message="用戶已存在")],
                                     error_messages={
                                         "blank": "请输入用户名称",
                                         "required": "用户名称不能为空",
                                         "max_length": "用户名称过长",
                                     })

    def get_admin(self, obj: UserProfile):
        role_list = obj.role.filter(status='1').values_list('admin', flat=True)
        if True in list(set(role_list)):
            return True
        return False

    def validate(self, attrs: dict):
        return super().validate(attrs)

    def save(self, **kwargs):
        self.validated_data['dept_id'] = self.initial_data.get('deptId', None)
        data = super().save(**kwargs)
        data.post.set(self.initial_data.get('postIds'))
        data.role.set(self.initial_data.get('roleIds'))
        return data

    def create(self, validated_data):
        data = super().create(validated_data)
        data.set_password(self.initial_data.get('password', None))
        data.save()
        return data

    class Meta:
        model = UserProfile
        exclude = ('password', 'secret', 'user_permissions', 'groups', 'is_superuser', 'date_joined')
        read_only_fields = ('dept',)


class UserProfileImportSerializer(CustomModelSerializer):

    def save(self, **kwargs):
        data = super().save(**kwargs)
        password = hashlib.new('md5', self.initial_data.get('password', '').encode(encoding='UTF-8')).hexdigest()
        data.set_password(password)
        data.save()
        return data

    def run_validation(self, data={}):
        # 把excel 数据进行格式转换
        if type(data) is dict:
            data['role'] = str(data['role']).split(',')
            data['post'] = str(data['post']).split(',')
            data['gender'] = {'男': '0', '女': '1', '未知': '2'}.get(data['gender'])
            data['is_active'] = {'启用': True, '禁用': False}.get(data['is_active'])
        return super().run_validation(data)

    class Meta:
        model = UserProfile
        exclude = ('password', 'secret', 'user_permissions', 'groups', 'is_superuser', 'date_joined')
