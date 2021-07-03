from django.db.models import CharField, ForeignKey, CASCADE

from apps.vadmin.op_drf.models import CoreModel


class Monitor(CoreModel):
    cpu_num = CharField(max_length=8, verbose_name='CPU核数')
    cpu_sys = CharField(max_length=8, verbose_name='CPU已使用率')
    mem_num = CharField(max_length=32, verbose_name='内存总数(KB)')
    mem_sys = CharField(max_length=32, verbose_name='内存已使用大小(KB)')
    seconds = CharField(max_length=32, verbose_name='系统已运行时间')
    server = ForeignKey(to='monitor.Server', on_delete=CASCADE, verbose_name="关联服务器信息", db_constraint=False)

    class Meta:
        verbose_name = '服务器监控信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.server and self.server.name and self.server.ip}监控信息"
