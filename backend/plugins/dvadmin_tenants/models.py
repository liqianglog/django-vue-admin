import datetime

from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

from application import dispatch
from dvadmin.utils.models import table_prefix
# 商城微信小程序


def auth_id():
    client = Client.objects.all().order_by('-id').values('id').first()
    return client.get('id', 100000) + 1


class Client(TenantMixin):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id", default=auth_id)
    name = models.CharField(max_length=100,  help_text="租户名称", verbose_name="租户名称",)
    on_trial = models.BooleanField(help_text="是否启用", verbose_name="是否启用")
    start_datetime = models.DateField(default=datetime.datetime.now, verbose_name="租户有效开始时间", help_text="租户有效开始时间")
    paid_until = models.DateField(help_text="租户有效截止时间", verbose_name="租户有效截止时间",)
    created_on = models.DateField(auto_now_add=True)
    auto_create_schema = True


    def __str__(self):
        return self.name

    def save(self, verbosity=1, *args, **kwargs):
        data = super().save(verbosity, *args, **kwargs)
        dispatch.refresh_system_config()  # 有更新则刷新系统配置
        return data

    class Meta:
        db_table = table_prefix + "tenant_client"
        verbose_name = '租户信息'
        verbose_name_plural = verbose_name
        ordering = ('start_datetime',)


class Domain(DomainMixin):

    def __str__(self):
        return self.domain

    class Meta:
        db_table = table_prefix + "tenant_domain"
        verbose_name = '租户domain'
        verbose_name_plural = verbose_name
        ordering = ('id',)
