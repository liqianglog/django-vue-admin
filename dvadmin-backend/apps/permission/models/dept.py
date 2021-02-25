from django.db.models import CASCADE
from django.db.models import CharField, IntegerField, BooleanField, ForeignKey

from apps.op_drf.models import CoreModel


class Dept(CoreModel):
    name = CharField(max_length=64, verbose_name="部门名称")
    orderNum = IntegerField(verbose_name="显示排序")
    owner = CharField(max_length=32, verbose_name="负责人", null=True)
    phone = CharField(max_length=32, verbose_name="联系电话", null=True)
    email = CharField(max_length=32, verbose_name="邮箱", null=True)
    status = BooleanField(default=False, verbose_name="部门状态")
    parentId = ForeignKey(to='Dept', on_delete=CASCADE, default=False, verbose_name="上级部门")

    class Meta:
        verbose_name = '部门管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"
