from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import UserManager, AbstractUser
from django.core.cache import cache
from django.db.models import IntegerField, ForeignKey, CharField, TextField, ManyToManyField, CASCADE

from apps.vadmin.op_drf.models import CoreModel


class UserProfile(AbstractUser, CoreModel):
    USER_TYPE_CHOICES = (
        (0, "后台用户"),
        (1, "前台用户"),
    )
    objects = UserManager()
    username = CharField(max_length=150, unique=True, db_index=True, verbose_name='用户账号')
    secret = CharField(max_length=255, default=uuid4, verbose_name='加密秘钥')
    email = CharField(max_length=255, verbose_name="邮箱", null=True, blank=True)
    mobile = CharField(max_length=255, verbose_name="电话", null=True, blank=True)
    avatar = TextField(verbose_name="头像", null=True, blank=True)
    name = CharField(max_length=40, verbose_name="姓名")
    gender = CharField(max_length=8, verbose_name="性别", null=True, blank=True)
    remark = TextField(verbose_name="备注", null=True)
    user_type = IntegerField(default=0, verbose_name="用户类型")
    post = ManyToManyField(to='permission.Post', verbose_name='关联岗位', db_constraint=False)
    role = ManyToManyField(to='permission.Role', verbose_name='关联角色', db_constraint=False)
    dept = ForeignKey(to='permission.Dept', verbose_name='归属部门', on_delete=CASCADE, db_constraint=False, null=True,
                      blank=True)

    @property
    def get_user_interface_dict(self):
        interface_dict = cache.get(f'permission_interface_dict_{self.username}', {}) if \
            getattr(settings, "REDIS_ENABLE", False) else {}
        if not interface_dict:
            for ele in self.role.filter(status='1', menu__status='1').values('menu__interface_path',
                                                                             'menu__interface_method').distinct():
                interface_path = ele.get('menu__interface_path')
                if interface_path is None or interface_path == '':
                    continue
                if ele.get('menu__interface_method') in interface_dict:
                    interface_dict[ele.get('menu__interface_method', '')].append(interface_path)
                else:
                    interface_dict[ele.get('menu__interface_method', '')] = [interface_path]
            if getattr(settings, "REDIS_ENABLE", False):
                cache.set(f'permission_interface_dict_{self.username}', interface_dict, 84600)
        return interface_dict

    @property
    def delete_cache(self):
        """
        清空缓存中的接口列表
        :return:
        """
        if not getattr(settings, "REDIS_ENABLE", False): return ""
        return cache.delete(f'permission_interface_dict_{self.username}')

    class Meta:
        abstract = settings.AUTH_USER_MODEL != 'permission.UserProfile'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.name:
            return f"{self.username}({self.name})"
        return f"{self.username}"
