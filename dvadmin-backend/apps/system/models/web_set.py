from django.db.models import TextField, CharField

from apps.op_drf.models import CoreModel


class WebSet(CoreModel):
    name = CharField(max_length=64, verbose_name="站点名称")
    web_site = CharField(max_length=256, verbose_name="站点网址", null=True)
    logo = CharField(max_length=256, verbose_name="网站Logo", null=True)
    record_info = TextField(verbose_name="备案信息", null=True)
    statistics_code = TextField(verbose_name="统计代码", null=True)
    copyright_info = TextField(verbose_name="版权信息", null=True)

    class Meta:
        verbose_name = '站点设置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"
