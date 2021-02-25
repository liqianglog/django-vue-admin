from django.db.models import IntegerField, BooleanField, CharField, TextField, ManyToManyField

from apps.op_drf.models import CoreModel


class Role(CoreModel):
    PURVIEW_CHOICES = (
        (0, "全部数据权限"),
        (1, "自定数据权限"),
        (2, "本部门数据权限"),
        (3, "本部门及以下数据权限"),
        (4, "仅本人数据权限"),
    )
    name = CharField(max_length=64, verbose_name="角色名称")
    roleKey = CharField(max_length=64, verbose_name="权限字符")
    orderNum = IntegerField(verbose_name="角色顺序")
    status = BooleanField(default=False, verbose_name="角色状态")
    admin = BooleanField(default=False, verbose_name="是否为admin")
    purview = IntegerField(default=0, choices=PURVIEW_CHOICES, verbose_name="权限范围")
    remark = TextField(verbose_name="备注", help_text="备注", null=True)
    dept = ManyToManyField(to='Dept', verbose_name='数据权限-关联部门')
    menu = ManyToManyField(to='Menu', verbose_name='关联菜单权限')

    class Meta:
        verbose_name = '角色管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"
