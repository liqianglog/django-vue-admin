from django.db.models import SET_DEFAULT

from utils import fields
from utils.BaseModels import CoreModel


class Dept(CoreModel):
    name = fields.CharField(null=False, max_length=64, verbose_name="部门名称")
    orderNum = fields.IntegerField(verbose_name="显示排序")
    owner = fields.CharField(max_length=32, verbose_name="负责人")
    phone = fields.CharField(max_length=32, verbose_name="联系电话")
    email = fields.CharField(max_length=32, verbose_name="邮箱")
    status = fields.BooleanField(default=False, verbose_name="部门状态")
    parentId = fields.ForeignKey(to='Dept', on_delete=SET_DEFAULT, default=False, verbose_name="上级部门")

    class Meta:
        verbose_name = '部门管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"
