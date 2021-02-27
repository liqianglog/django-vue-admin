from uuid import uuid4

from django.contrib.auth.models import UserManager, AbstractUser
from django.db.models import IntegerField, ForeignKey, CharField, TextField, ManyToManyField, CASCADE

from apps.op_drf.fields import CreateDateTimeField, UpdateDateTimeField


class UserProfile(AbstractUser):
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
    post = ManyToManyField(to='Post', verbose_name='关联岗位', db_constraint=False)
    role = ManyToManyField(to='Role', verbose_name='关联角色', db_constraint=False)
    dept = ForeignKey(to='Dept', verbose_name='归属部门', on_delete=CASCADE, db_constraint=False, null=True, blank=True)
    create_datetime = CreateDateTimeField()
    update_datetime = UpdateDateTimeField()

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.name:
            return f"{self.username}({self.name})"
        return f"{self.username}"
