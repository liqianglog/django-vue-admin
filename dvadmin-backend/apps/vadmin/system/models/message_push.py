from django.conf import settings
from django.db import models
from django.db.models import *

from apps.vadmin.op_drf.fields import UpdateDateTimeField, CreateDateTimeField
from apps.vadmin.op_drf.models import CoreModel

"""
消息通知模型
"""


class MessagePush(CoreModel):
    title = CharField(max_length=128, verbose_name="通知标题")
    content = TextField(verbose_name="通知内容")
    message_type = CharField(max_length=8, verbose_name="通知类型")
    is_reviewed = BooleanField(default=True, verbose_name="是否审核")
    status = CharField(max_length=8, verbose_name="通知状态")
    to_path = CharField(max_length=256, verbose_name="跳转路径", null=True, blank=True, )
    user = ManyToManyField(to=settings.AUTH_USER_MODEL,
                           related_name="user", related_query_name="user_query", through='MessagePushUser',
                           through_fields=('message_push', 'user'))

    class Meta:
        verbose_name = '通知公告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.title}"


class MessagePushUser(models.Model):
    message_push = ForeignKey(MessagePush, on_delete=CASCADE, db_constraint=False,
                              related_name="messagepushuser_message_push",
                              verbose_name='消息通知', help_text='消息通知')

    user = ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=CASCADE, db_constraint=False,
                      related_name="messagepushuser_user",
                      verbose_name='用户', help_text='用户')
    is_read = BooleanField(default=False, verbose_name="是否已读")
    update_datetime = UpdateDateTimeField()  # 修改时间
    create_datetime = CreateDateTimeField()  # 创建时间

    class Meta:
        verbose_name = "通知公告与用户关系"
        verbose_name_plural = verbose_name
