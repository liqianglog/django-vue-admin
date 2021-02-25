from django.db.models import CharField, ForeignKey, BooleanField, CASCADE

from apps.op_drf.models import CoreModel


class ConfigSettings(CoreModel):
    name = CharField(max_length=64, verbose_name="参数名称")
    configKey = CharField(max_length=256, verbose_name="参数键名")
    configValue = CharField(max_length=256, verbose_name="参数键值")
    configType = BooleanField(default=False,verbose_name="是否内置")
    is_status = BooleanField(default=False, verbose_name="字典状态")
    sort = CharField(max_length=256, verbose_name="字典排序")
    dict_data = ForeignKey(to='DictData', on_delete=CASCADE, verbose_name="关联字典")
    remark = CharField(max_length=256, verbose_name="备注", null=True)

    class Meta:
        verbose_name = '参数设置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"
