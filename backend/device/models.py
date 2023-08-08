from django.db import models

from dvadmin.utils.models import CoreModel, table_prefix


class Template(CoreModel):
    CLASSIFY_CHOICE = (
        (0, "网关"),
        (1, "终端设备"),
    )
    classify = models.SmallIntegerField(choices=CLASSIFY_CHOICE, verbose_name="模板类别")
    name = models.CharField(max_length=128, verbose_name="模板名称", unique=True)

    class Meta:
        db_table = table_prefix + 'device_template'
        verbose_name = "模板表"
        verbose_name_plural = verbose_name
        ordering = ("-id",)


class TemplateDetail(CoreModel):
    template = models.ForeignKey(to="Template", null=False, on_delete=models.CASCADE, db_constraint=False,
                                 verbose_name="所属模板")
    key_title = models.CharField(max_length=64, verbose_name="键标题", unique=True)
    key_name = models.CharField(max_length=64, verbose_name="键名")
    key_type = models.CharField(max_length=32, verbose_name="键值类型")
    parent_key = models.ForeignKey(to="TemplateDetail", null=True, on_delete=models.CASCADE, db_constraint=False,
                                   verbose_name="父级键")

    class Meta:
        db_table = table_prefix + 'device_template_detail'
        verbose_name = "模板详情表"
        verbose_name_plural = verbose_name
        ordering = ("-id",)
        unique_together = (('key_name', 'parent_key'),)


class Gateway(CoreModel):
    name = models.CharField(max_length=128, verbose_name="设备名称", unique=True)
    specification = models.CharField(max_length=32, verbose_name="设备型号")
    mac_address = models.CharField(max_length=32, verbose_name="设备MAC地址")
    version = models.CharField(max_length=64, verbose_name="设备固件版本号")
    ip_address = models.CharField(max_length=32, verbose_name="设备IP地址")
    physics_address = models.CharField(max_length=255, default="暂无位置信息", verbose_name="设备实际地址")
    account = models.CharField(max_length=32, verbose_name="设备账号")
    password = models.CharField(max_length=32, verbose_name="设备密码")
    template = models.ForeignKey(to="Template", null=False, on_delete=models.CASCADE, db_constraint=False,
                                 verbose_name="所用模板")

    class Meta:
        db_table = table_prefix + 'device_gateways'
        verbose_name = "网关表"
        verbose_name_plural = verbose_name
        ordering = ("-id",)


class Terminal(CoreModel):
    name = models.CharField(max_length=128, verbose_name="设备名称", unique=True)
    specification = models.CharField(max_length=32, verbose_name="设备型号")
    identify = models.CharField(max_length=128, verbose_name="设备标识", unique=True)
    physics_address = models.CharField(max_length=255, default="暂无位置信息", verbose_name="设备实际地址")
    project = models.CharField(max_length=128, verbose_name="所属项目")
    remark = models.CharField(max_length=255, null=True, verbose_name="设备备注")
    gateway = models.ForeignKey(to=Gateway, null=True, on_delete=models.CASCADE, db_constraint=False,
                                verbose_name="关联网关")
    template = models.ForeignKey(to="Template", null=False, on_delete=models.CASCADE, db_constraint=False,
                                 verbose_name="所用模板")

    class Meta:
        db_table = table_prefix + 'device_terminal'
        verbose_name = "终端设备表"
        verbose_name_plural = verbose_name
        ordering = ("-id",)
