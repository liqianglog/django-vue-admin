import random

from django.db import models, connection
from django.db.models import CASCADE

from dvadmin.system.models import Users
from dvadmin.utils.models import CoreModel
from dvadmin.utils.string_util import random_str
from dvadmin_tenants.models import Client

table_prefix = "carton_"

STATUS_CHOICES = (
    (0, "失效"),
    (1, "有效"),
)


class FactoryInfo(CoreModel):
    code = models.CharField(max_length=50, verbose_name="编号", help_text="编号", unique=True, db_index=True, )
    name = models.CharField(max_length=30, verbose_name="工厂名称", help_text="工厂名称")
    contacts = models.CharField(max_length=20, verbose_name="联系人", help_text="联系人", null=True, blank=True)
    telephone = models.CharField(max_length=20, verbose_name="手机号码", help_text="手机号码", null=True, blank=True)
    address = models.CharField(max_length=200, verbose_name="详细地址", help_text="详细地址", null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="状态", help_text="状态")

    class Meta:
        db_table = table_prefix + "factory_info"
        verbose_name = '工厂'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

    def __str__(self):
        return f"{self.name}"


class ProductionLine(CoreModel):
    code = models.CharField(max_length=50, verbose_name="编号", help_text="编号", null=True, blank=True, unique=True,
                            db_index=True)
    name = models.CharField(max_length=20, verbose_name="产线名称", help_text="产线名称")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="状态", help_text="状态")
    belong_to_factory = models.ForeignKey(to='FactoryInfo', on_delete=CASCADE, related_name='factory_info',
                                          verbose_name="归属工厂", db_constraint=False,
                                          help_text="归属工厂", null=True, blank=True, )

    class Meta:
        db_table = table_prefix + "production_line"
        verbose_name = '产线'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

    def __str__(self):
        return f"{self.name}"


def default_code():
    client = Client.objects.filter(schema_name=connection.tenant.schema_name).first()
    schema_id = client.id
    return f"{schema_id}{random_str(number=8)}"


def default_bind_pwd():
    return random.randint(10000000, 99999999)


class DeviceManage(CoreModel):
    name = models.CharField(max_length=50, help_text="设备名称", verbose_name="设备名称")
    no = models.CharField(max_length=100, unique=True, blank=True, default=default_code, help_text="编号",
                          verbose_name="编号")
    password = models.CharField(max_length=100, blank=True, default=default_bind_pwd, help_text="设备登录密码",
                                verbose_name="设备登录密码")
    CHOICES_LIST = (
        (0, "闲置中"),
        (1, "生产中"),
        (2, "维护中")
    )
    production_status = models.IntegerField(choices=CHOICES_LIST, default=0, help_text="生产状态",
                                            verbose_name="生产状态")
    TYPE_LIST = (
        (0, "码包管理端"),
        (1, "检测管理端")
    )
    type = models.IntegerField(choices=TYPE_LIST, default=0, help_text="设备类型", verbose_name="设备类型")
    user = models.ForeignKey(Users, db_constraint=False, related_name="user_device", on_delete=models.CASCADE,
                             blank=True,
                             help_text="操作用户", verbose_name="操作用户")
    production_line = models.ForeignKey(ProductionLine, db_constraint=False, related_name="device_prodline",
                                        on_delete=models.CASCADE, help_text="所属产线", verbose_name="所属产线")

    class Meta:
        db_table = table_prefix + "device_manage"
        verbose_name = '生产设备管理'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

    def __str__(self):
        return str(self.name)


CODE_SOURCE = (
    (0, "透云"),
    (1, "信码新创"),
    (2, "其他")
)
LINE_FEED = (
    (0, "换行"),
    (1, "回车换行")
)
CODE_TYPE = (
    (0, "外码"),
    (1, "内码"),
    (2, "外码+内码")
)


class CodePackageTemplate(CoreModel):
    no = models.CharField(max_length=100, unique=True, help_text="编号", verbose_name="编号")
    name = models.CharField(max_length=50, null=True, blank=True, help_text="名称", verbose_name="名称")
    code_version = models.CharField(max_length=50, null=True, blank=True, help_text="模板版号", verbose_name="模板版号")
    code_source = models.IntegerField(choices=CODE_SOURCE, default=1, blank=True, help_text="编码来源",
                                      verbose_name="编码来源")
    separator = models.CharField(max_length=20, blank=True, default=",", help_text="分隔符", verbose_name="分隔符")
    fields = models.IntegerField(default=0, blank=True, help_text="字段数", verbose_name="字段数")
    char_length = models.IntegerField(default=0, blank=True, help_text="字符长度", verbose_name="字符长度")
    line_feed = models.IntegerField(choices=LINE_FEED, help_text="换行符", verbose_name="换行符")
    code_type = models.IntegerField(choices=CODE_TYPE, help_text="码类型", verbose_name="码类型")
    w_url_prefix = models.CharField(max_length=200, help_text="外码地址", verbose_name="外码地址")
    w_url_length = models.IntegerField(default=0, help_text="外码长度", verbose_name="外码长度")
    w_field_position = models.IntegerField(default=0, help_text="外码位置", verbose_name="外码位置")
    n_url_prefix = models.CharField(max_length=200, help_text="内码地址", verbose_name="内码地址")
    n_url_length = models.IntegerField(default=0, help_text="内码长度", verbose_name="内码长度")
    n_field_position = models.IntegerField(default=0, help_text="内码位置", verbose_name="内码位置")

    class Meta:
        db_table = table_prefix + "code_package_template"
        verbose_name = '码包模板'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)
