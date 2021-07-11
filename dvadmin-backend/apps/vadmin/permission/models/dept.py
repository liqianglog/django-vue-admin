from django.db.models import CASCADE
from django.db.models import CharField, IntegerField, ForeignKey

from apps.vadmin.op_drf.models import CoreModel


class Dept(CoreModel):
    deptName = CharField(max_length=64, verbose_name="部门名称")
    orderNum = IntegerField(verbose_name="显示排序")
    owner = CharField(max_length=32, verbose_name="负责人", null=True, blank=True)
    phone = CharField(max_length=32, verbose_name="联系电话", null=True, blank=True)
    email = CharField(max_length=32, verbose_name="邮箱", null=True, blank=True)
    status = CharField(max_length=8, verbose_name="部门状态", null=True, blank=True)
    parentId = ForeignKey(to='permission.Dept', on_delete=CASCADE, default=False, verbose_name="上级部门",
                          db_constraint=False, null=True, blank=True)

    class Meta:
        verbose_name = '部门管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.deptName}"
