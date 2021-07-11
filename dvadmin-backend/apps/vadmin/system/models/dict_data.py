from django.db.models import TextField, CharField,ForeignKey

from apps.vadmin.op_drf.models import CoreModel


class DictData(CoreModel):
    dictName = CharField(max_length=64, verbose_name="字典名称")
    dictType = CharField(max_length=64, verbose_name="字典类型")
    status = CharField(max_length=8, verbose_name="字典状态")
    remark = CharField(max_length=256,verbose_name="备注", null=True, blank=True)

    class Meta:
        verbose_name = '字典管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.dictName}"
