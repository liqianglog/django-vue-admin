from django.db import models

from .fields import CreateDateTimeField, DescriptionField, CreatorCharField, \
    ModifierCharField, UpdateDateTimeField


class BaseModel(models.Model):
    """
    标准抽象模型模型,可直接继承使用
    """
    description = DescriptionField()  # 描述
    update_datetime = UpdateDateTimeField()  # 修改时间
    create_datetime = CreateDateTimeField()  # 创建时间

    class Meta:
        abstract = True
        verbose_name = '基本模型'
        verbose_name_plural = verbose_name


class CoreModel(models.Model):
    """
    核心标准抽象模型模型,可直接继承使用
    增加审计字段, 覆盖字段时, 字段名称请勿修改, 必须统一审计字段名称
    """
    description = DescriptionField()  # 描述
    creator = CreatorCharField()  # 创建者
    modifier = ModifierCharField()  # 修改者
    update_datetime = UpdateDateTimeField()  # 修改时间
    create_datetime = CreateDateTimeField()  # 创建时间

    class Meta:
        abstract = True
        verbose_name = '核心模型'
        verbose_name_plural = verbose_name
