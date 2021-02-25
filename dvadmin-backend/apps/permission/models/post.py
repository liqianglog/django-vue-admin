from django.db.models import IntegerField, BooleanField, CharField, TextField

from apps.op_drf.models import CoreModel


class Post(CoreModel):
    name = CharField(null=False, max_length=64, verbose_name="岗位名称")
    web_path = CharField(max_length=32, verbose_name="岗位编码")
    orderNum = IntegerField(verbose_name="岗位顺序")
    status = BooleanField(default=False, verbose_name="岗位状态")
    remark = TextField(verbose_name="备注", help_text="备注", null=True)

    class Meta:
        verbose_name = '岗位管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"
