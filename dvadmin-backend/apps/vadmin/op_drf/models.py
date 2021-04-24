from django.conf import settings
from django.db import models
from django.db.models import SET_NULL

from .fields import CreateDateTimeField, DescriptionField, ModifierCharField, UpdateDateTimeField


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
    creator = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_query_name='creator_query', null=True,
                                verbose_name='创建者', on_delete=SET_NULL, db_constraint=False)  # 创建者
    modifier = ModifierCharField()  # 修改者
    dept_belong_id = models.CharField(max_length=64, verbose_name="数据归属部门", null=True, blank=True)
    update_datetime = UpdateDateTimeField()  # 修改时间
    create_datetime = CreateDateTimeField()  # 创建时间

    class Meta:
        abstract = True
        verbose_name = '核心模型'
        verbose_name_plural = verbose_name
