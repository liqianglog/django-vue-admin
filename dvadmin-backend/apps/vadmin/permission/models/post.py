from django.db.models import IntegerField, BooleanField, CharField, TextField

from apps.vadmin.op_drf.models import CoreModel


class Post(CoreModel):
    postName = CharField(null=False, max_length=64, verbose_name="岗位名称")
    postCode = CharField(max_length=32, verbose_name="岗位编码")
    postSort = IntegerField(verbose_name="岗位顺序")
    status = CharField(max_length=8, verbose_name="岗位状态")
    remark = TextField(verbose_name="备注", help_text="备注", null=True, blank=True)

    class Meta:
        verbose_name = '岗位管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.postName}"
