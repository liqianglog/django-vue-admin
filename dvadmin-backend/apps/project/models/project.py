from django.conf import settings
from django.db.models import CharField, ForeignKey, CASCADE, SET_NULL

from vadmin.op_drf.models import CoreModel


# 继承框架封装的 模型类 CoreModel
class Project(CoreModel):
    name = CharField(max_length=8, verbose_name='项目名称')
    code = CharField(max_length=8, verbose_name='项目编码')
    # 在关联用户时，建议使用 to=settings.AUTH_USER_MODEL 进行关联
    person = ForeignKey(to=settings.AUTH_USER_MODEL, null=True, verbose_name='项目负责人', related_name='project_person',
                        on_delete=SET_NULL, db_constraint=False)
    # 在普通一多一、一对多、多对多时，to='App名.模块名' 进行关联
    dept = ForeignKey(to='permission.dept', on_delete=CASCADE, verbose_name="项目所属部门", related_name='project_dept',
                      db_constraint=False)

    class Meta:
        verbose_name = '项目管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name} 项目"
