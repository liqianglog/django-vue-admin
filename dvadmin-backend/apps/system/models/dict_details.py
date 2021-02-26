from django.db.models import CharField, ForeignKey, BooleanField, CASCADE

from apps.op_drf.models import CoreModel


class DictDetails(CoreModel):
    dictLabel = CharField(max_length=64, verbose_name="字典标签")
    dictValue = CharField(max_length=256, verbose_name="字典键值")
    is_default = BooleanField(verbose_name="是否默认", default=False)
    status = CharField(max_length=2, verbose_name="字典状态")
    sort = CharField(max_length=256, verbose_name="字典排序")
    dict_data = ForeignKey(to='DictData', on_delete=CASCADE, verbose_name="关联字典")
    remark = CharField(max_length=256, verbose_name="备注", null=True)

    class Meta:
        verbose_name = '字典详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.dictLabel}"
