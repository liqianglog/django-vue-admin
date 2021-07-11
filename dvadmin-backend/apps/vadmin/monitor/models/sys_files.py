from django.db.models import CharField, ForeignKey, CASCADE

from apps.vadmin.op_drf.models import CoreModel


class SysFiles(CoreModel):
    dir_name = CharField(max_length=32, verbose_name='磁盘路径')
    sys_type_name = CharField(max_length=400, verbose_name='系统文件类型')
    type_name = CharField(max_length=32, verbose_name='盘符类型')
    total = CharField(max_length=32, verbose_name='磁盘总大小(KB)')
    disk_sys = CharField(max_length=32, verbose_name='已使用大小(KB)')
    monitor = ForeignKey(to='monitor.Monitor', on_delete=CASCADE, verbose_name="关联服务器监控信息", db_constraint=False)

    class Meta:
        verbose_name = '系统磁盘'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.creator and self.creator.name}"
