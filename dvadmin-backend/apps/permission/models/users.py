from uuid import uuid4

from django.contrib.auth.models import UserManager, AbstractUser

from utils import fields


class UserProfile(AbstractUser):
    GENDER_CHOICES = (
        (0, "女"),
        (1, "男"),
        (2, "未知"),
    )
    USER_TYPE_CHOICES = (
        (0, "后台用户"),
        (1, "前台用户"),
    )
    objects = UserManager()
    username = fields.CharField(max_length=150, unique=True, db_index=True, verbose_name='用户账号')
    secret = fields.CharField(max_length=255, default=uuid4, verbose_name='加密秘钥')
    email = fields.CharField(max_length=255, verbose_name="邮箱")
    mobile = fields.CharField(max_length=255, verbose_name="电话")
    avatar = fields.TextField(verbose_name="头像")
    name = fields.CharField(max_length=40, verbose_name="姓名")
    gender = fields.IntegerField(default=2, choices=GENDER_CHOICES, verbose_name="性别")
    remark = fields.TextField(verbose_name="备注")
    user_type = fields.IntegerField(default=2, choices=GENDER_CHOICES, verbose_name="用户类型")
    post = fields.ForeignKey(to='Post', verbose_name='关联岗位')
    role = fields.ForeignKey(to='Role', verbose_name='关联角色')
    dept = fields.ForeignKey(to='Dept', verbose_name='归属部门')
    create_datetime = fields.CreateDateTimeField()
    update_datetime = fields.UpdateDateTimeField()

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.name:
            return f"{self.username}({self.name})"
        return f"{self.username}"
