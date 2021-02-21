from uuid import uuid4

from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    GENDER_CHOICES = (
        ("女", "女"),
        ("男", "男"),
        ("未知", "未知"),
    )
    objects = UserManager()
    username = models.CharField(max_length=150, unique=True, db_index=True,
                                verbose_name='username', help_text='用户昵称')
    secret = models.CharField(max_length=255, default=uuid4, verbose_name='加密秘钥')
    email = models.CharField(max_length=255, null=True, blank=True, verbose_name="邮箱")
    mobile = models.CharField(max_length=255, null=True, blank=True, verbose_name="电话")
    avatar = models.TextField(null=True, blank=True, verbose_name="头像", help_text="头像")

    name = models.CharField(max_length=40, unique=False, null=True,
                            blank=True, verbose_name="姓名")
    gender = models.CharField(max_length=2, default=GENDER_CHOICES[2][0], choices=GENDER_CHOICES,
                              verbose_name="性别", help_text="性别")
    remark = models.TextField(null=True, blank=True, verbose_name="备注", help_text="备注")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True,
                                           verbose_name=u'创建时间', help_text=u"创建时间")
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True,
                                           verbose_name=u'更新时间', help_text=u"更新时间")

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.name:
            return f"{self.username}({self.name})"
        return f"{self.username}"
