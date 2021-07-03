from django.db.models import CharField, ForeignKey, BooleanField, CASCADE

from apps.vadmin.op_drf.models import CoreModel


class ConfigSettings(CoreModel):
    configName = CharField(max_length=64, verbose_name="参数名称")
    configKey = CharField(max_length=256, verbose_name="参数键名")
    configValue = CharField(max_length=256, verbose_name="参数键值")
    configType = CharField(max_length=8,verbose_name="是否内置")
    status = CharField(max_length=8, verbose_name="参数状态")
    remark = CharField(max_length=256, verbose_name="备注", null=True, blank=True)

    class Meta:
        verbose_name = '参数设置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.configName}"
