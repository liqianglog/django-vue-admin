from django.db.models import IntegerField, BooleanField, CharField, TextField, ManyToManyField

from apps.vadmin.op_drf.models import CoreModel


class Role(CoreModel):
    DATASCOPE_CHOICES = (
        ('1', "全部数据权限"),
        ('2', "自定数据权限"),
        ('3', "本部门数据权限"),
        ('4', "本部门及以下数据权限"),
        ('5', "仅本人数据权限"),
    )
    roleName = CharField(max_length=64, verbose_name="角色名称")
    roleKey = CharField(max_length=64, verbose_name="权限字符")
    roleSort = IntegerField(verbose_name="角色顺序")
    status = CharField(max_length=8, verbose_name="角色状态")
    admin = BooleanField(default=False, verbose_name="是否为admin")
    dataScope = CharField(max_length=8, default='1', choices=DATASCOPE_CHOICES, verbose_name="权限范围", )
    remark = TextField(verbose_name="备注", help_text="备注", null=True, blank=True)
    dept = ManyToManyField(to='permission.Dept', verbose_name='数据权限-关联部门', db_constraint=False)
    menu = ManyToManyField(to='permission.Menu', verbose_name='关联菜单权限', db_constraint=False)

    class Meta:
        verbose_name = '角色管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.roleName}"
