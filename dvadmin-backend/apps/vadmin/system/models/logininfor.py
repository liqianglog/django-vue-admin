from django.db.models import CharField, BooleanField, TextField

from apps.vadmin.op_drf.models import CoreModel


class LoginInfor(CoreModel):
    session_id = CharField(max_length=64, verbose_name="会话标识", null=True, blank=True)
    browser = CharField(max_length=64, verbose_name="浏览器")
    ipaddr = CharField(max_length=32, verbose_name="ip地址", null=True, blank=True)
    loginLocation = CharField(max_length=64, verbose_name="登录位置", null=True, blank=True)
    msg = TextField(verbose_name="操作信息", null=True, blank=True)
    os = CharField(max_length=64, verbose_name="操作系统", null=True, blank=True)
    status = BooleanField(default=False, verbose_name="登录状态")

    class Meta:
        verbose_name = '登录日志'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.creator and self.creator.name}"
