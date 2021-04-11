from django.db import models
from django.db.models import CharField

from apps.vadmin.op_drf.fields import UpdateDateTimeField, CreateDateTimeField


class Server(models.Model):
    name = CharField(max_length=256, verbose_name='服务器名称', null=True, blank=True)
    ip = CharField(max_length=32, verbose_name="ip地址")
    os = CharField(max_length=32, verbose_name="操作系统")
    remark = CharField(max_length=256, verbose_name="备注", null=True, blank=True)
    update_datetime = UpdateDateTimeField()  # 修改时间
    create_datetime = CreateDateTimeField()  # 创建时间

    class Meta:
        verbose_name = '服务器信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name and self.ip}"
