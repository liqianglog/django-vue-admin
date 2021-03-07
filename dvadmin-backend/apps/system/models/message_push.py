from django.db.models import *

from apps.op_drf.models import CoreModel

"""
消息通知模型
"""


class MessagePush(CoreModel):
    content = TextField(verbose_name="通知内容")
    title = CharField(max_length=128, verbose_name="通知标题")
    is_read = BooleanField(default=False, verbose_name="是否已读")
    message_type = CharField(max_length=64, verbose_name="消息类型")
    is_reviewed = BooleanField(default=False, verbose_name="是否审核")
    is_send = BooleanField(default=False, verbose_name="是否已发送")
    recipient_id = ManyToManyField(to="permission.UserProfile", db_constraint=False, null=True, blank=True,
                                   related_name="recipient", related_query_name="recipient_query")

    class Meta:
        verbose_name = '消息通知'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.title}"
