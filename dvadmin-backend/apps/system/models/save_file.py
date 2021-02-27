import os
import uuid

from django.db.models import CharField, FileField
from django.utils import timezone

from apps.op_drf.models import CoreModel


def files_path(instance, filename):
    return '/'.join(['system', timezone.now().strftime("%Y-%m-%d"), str(uuid.uuid4()) + os.path.splitext(filename)[-1]])


class SaveFile(CoreModel):
    name = CharField(max_length=128, verbose_name="文件名称", null=True, blank=True)
    type = CharField(max_length=32, verbose_name="文件类型", null=True, blank=True)
    size = CharField(max_length=64, verbose_name="文件大小", null=True, blank=True)
    address = CharField(max_length=16, verbose_name="存储位置", null=True, blank=True)  # 本地、阿里云、腾讯云..
    oss_url = CharField(max_length=200, verbose_name="OSS地址", null=True, blank=True)
    file = FileField(verbose_name="文件URL", upload_to=files_path, )

    class Meta:
        verbose_name = '文件管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"
