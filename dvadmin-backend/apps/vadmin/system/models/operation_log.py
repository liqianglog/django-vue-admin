from django.db.models import TextField, CharField, BooleanField

from apps.vadmin.op_drf.models import CoreModel


class OperationLog(CoreModel):
    request_modular = CharField(max_length=64, verbose_name="请求模块", null=True, blank=True)
    request_path = CharField(max_length=400, verbose_name="请求地址", null=True, blank=True)
    request_body = TextField(verbose_name="请求参数", null=True, blank=True)
    request_method = CharField(max_length=64, verbose_name="请求方式", null=True, blank=True)
    request_msg = TextField(verbose_name="操作说明", null=True, blank=True)
    request_ip = CharField(max_length=32, verbose_name="请求ip地址", null=True, blank=True)
    request_browser = CharField(max_length=64, verbose_name="请求浏览器", null=True, blank=True)
    response_code = CharField(max_length=32, verbose_name="响应状态码", null=True, blank=True)
    request_location = CharField(max_length=64, verbose_name="操作地点", null=True, blank=True)
    request_os = CharField(max_length=64, verbose_name="操作系统", null=True, blank=True)
    json_result = TextField(verbose_name="返回信息", null=True, blank=True)
    status = BooleanField(default=False, verbose_name="响应状态")

    class Meta:
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.request_msg}[{self.request_modular}]"
