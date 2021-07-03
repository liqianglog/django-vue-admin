from django.db.models import CharField, BooleanField, TextField

from apps.vadmin.op_drf.models import CoreModel


class CeleryLog(CoreModel):
    name = CharField(max_length=256, verbose_name='任务名称', help_text='任务名称')
    func_name = CharField(max_length=256, verbose_name='执行函数名称', help_text='执行函数名称')
    kwargs = TextField(max_length=1024, verbose_name='执行参数', help_text='运行参数')
    seconds = CharField(max_length=8, verbose_name='执行时间')
    status = BooleanField(default=False, verbose_name='运行状态')
    result = TextField(max_length=10240, verbose_name='任务结果', help_text='任务返回内容')

    class Meta:
        verbose_name = 'celery定时日志'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.creator and self.creator.name}"
