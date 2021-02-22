from utils import fields
from utils.BaseModels import CoreModel


class Role(CoreModel):
    PURVIEW_CHOICES = (
        (0, "全部数据权限"),
        (1, "自定数据权限"),
        (2, "本部门数据权限"),
        (3, "本部门及以下数据权限"),
        (4, "仅本人数据权限"),
    )
    name = fields.CharField(null=False, max_length=64, verbose_name="角色名称")
    orderNum = fields.IntegerField(verbose_name="角色顺序")
    status = fields.BooleanField(default=False, verbose_name="角色状态")
    purview = fields.IntegerField(default=0, choices=PURVIEW_CHOICES, verbose_name="权限范围")
    remark = fields.TextField(verbose_name="备注", help_text="备注")
    dept = fields.ManyToManyField(to='Dept', verbose_name='数据权限-关联部门')
    menu = fields.ManyToManyField(to='Menu', verbose_name='关联菜单权限')

    class Meta:
        verbose_name = '角色管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"
