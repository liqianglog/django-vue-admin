# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/5/31 031 22:08
@Remark: 公共基础model类
"""
import uuid
from datetime import date, timedelta

from django.apps import apps
from django.db import models, connection, ProgrammingError
from django.db.models import QuerySet

from application import settings
from application.dispatch import is_tenants_mode

table_prefix = settings.TABLE_PREFIX  # 数据库表名前缀


class SoftDeleteQuerySet(QuerySet):
    pass




class SoftDeleteManager(models.Manager):
    """支持软删除"""

    def __init__(self, *args, **kwargs):
        self.__add_is_del_filter = False
        super(SoftDeleteManager, self).__init__(*args, **kwargs)

    def filter(self, *args, **kwargs):
        # 考虑是否主动传入is_deleted
        if not kwargs.get('is_deleted') is None:
            self.__add_is_del_filter = True
        return super(SoftDeleteManager, self).filter(*args, **kwargs)

    def get_queryset(self):
        if self.__add_is_del_filter:
            return SoftDeleteQuerySet(self.model, using=self._db).exclude(is_deleted=False)
        return SoftDeleteQuerySet(self.model).exclude(is_deleted=True)

    def get_by_natural_key(self, name):
        return SoftDeleteQuerySet(self.model).get(username=name)


def get_month_range(start_day, end_day):
    months = (end_day.year - start_day.year) * 12 + end_day.month - start_day.month
    month_range = ['%s-%s-01' % (start_day.year + mon // 12, str(mon % 12 + 1).zfill(2))
                   for mon in range(start_day.month - 1, start_day.month + months)]
    return month_range


class SoftDeleteModel(models.Model):
    """
    软删除模型
    一旦继承,就将开启软删除
    """
    is_deleted = models.BooleanField(verbose_name="是否软删除", help_text='是否软删除', default=False, db_index=True)
    objects = SoftDeleteManager()

    class Meta:
        abstract = True
        verbose_name = '软删除模型'
        verbose_name_plural = verbose_name

    def delete(self, using=None, soft_delete=True, *args, **kwargs):
        """
        重写删除方法,直接开启软删除
        """
        self.is_deleted = True
        self.save(using=using)


class CoreModel(models.Model):
    """
    核心标准抽象模型模型,可直接继承使用
    增加审计字段, 覆盖字段时, 字段名称请勿修改, 必须统一审计字段名称
    """
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id")
    description = models.CharField(max_length=255, verbose_name="描述", null=True, blank=True, help_text="描述")
    creator = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_query_name='creator_query', null=True,
                                verbose_name='创建人', help_text="创建人", on_delete=models.SET_NULL,
                                db_constraint=False)
    modifier = models.CharField(max_length=255, null=True, blank=True, help_text="修改人", verbose_name="修改人")
    dept_belong_id = models.CharField(max_length=255, help_text="数据归属部门", null=True, blank=True,
                                      verbose_name="数据归属部门")
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间",
                                           verbose_name="修改时间")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",
                                           verbose_name="创建时间")

    class Meta:
        abstract = True
        verbose_name = '核心模型'
        verbose_name_plural = verbose_name


class AddPostgresPartitionedBase:
    """
    pgsql表分表基类
    """

    @classmethod
    def add_hash_partition(cls, number=36):
        """
        创建分区表
        :return:
        """
        if cls.PartitioningMeta.method != 'hash':
            raise ProgrammingError("表分区错误，无法进行分区")
        schema_editor = connection.schema_editor()
        if is_tenants_mode():
            schema_editor.sql_add_hash_partition = f'CREATE TABLE "{connection.tenant.schema_name}".%s PARTITION OF "{connection.tenant.schema_name}".%s FOR VALUES WITH (MODULUS %s, REMAINDER %s)'
        for item in range(number):
            try:
                schema_editor.add_hash_partition(
                    model=cls,
                    name="_" + str(item),
                    modulus=number,
                    remainder=item,
                )
            except ProgrammingError as e:
                print(f"{cls.__name__}分表失败：" + str(e).rstrip('\n'))
        return

    @classmethod
    def add_range_day_partition(cls, day=7):
        """
        按照创建时间"天"分表
        :return:
        """
        if cls.PartitioningMeta.method != 'range':
            raise ProgrammingError("表分区错误，无法进行分区")
        day_before = date.today().strftime("%Y-%m-%d")
        schema_editor = connection.schema_editor()
        if is_tenants_mode():
            schema_editor.sql_add_range_partition = (
                f'CREATE TABLE "{connection.tenant.schema_name}".%s PARTITION OF "{connection.tenant.schema_name}".%s FOR VALUES FROM (%s) TO (%s)'
            )
        for index in range(day):
            try:
                day_following = (date.today() + timedelta(days=index + 1)).strftime("%Y-%m-%d")
                schema_editor.add_range_partition(
                    model=cls,
                    name=f"{day_before}_{day_following}",
                    from_values=day_before,
                    to_values=day_following,
                )
                day_before = day_following
            except ProgrammingError as e:
                print(f"{cls.__name__}分表失败：" + str(e).rstrip('\n'))
        return

    @classmethod
    def add_range_month_partition(cls, start_date, end_date):
        """
        按照创建时间"月"分表
        :return:
        """
        if cls.PartitioningMeta.method != 'range':
            raise ProgrammingError("表分区错误，无法进行分区")
        range_month_partition_list = get_month_range(start_date, end_date)
        schema_editor = connection.schema_editor()
        if is_tenants_mode():
            schema_editor.sql_add_range_partition = (
                f'CREATE TABLE "{connection.tenant.schema_name}".%s PARTITION OF "{connection.tenant.schema_name}".%s FOR VALUES FROM (%s) TO (%s)'
            )
        for index, ele in enumerate(range_month_partition_list):
            if index == 0:
                continue
            try:
                schema_editor.add_range_partition(
                    model=cls,
                    name=f"{range_month_partition_list[index - 1][:-3]}_{ele[:-3]}",
                    from_values=range_month_partition_list[index - 1],
                    to_values=ele,
                )
            except ProgrammingError as e:
                print(f"{cls.__name__}分表失败：" + str(e).rstrip('\n'))
        return

    @classmethod
    def add_list_partition(cls, unique_value):
        """
        按照某个值进行分区
        :param unique_value:
        :return:
        """
        if cls.PartitioningMeta.method != 'list':
            raise ProgrammingError("表分区错误，无法进行分区")
        schema_editor = connection.schema_editor()
        if is_tenants_mode():
            schema_editor.sql_add_list_partition = (
                f'CREATE TABLE "{connection.tenant.schema_name}".%s PARTITION OF "{connection.tenant.schema_name}".%s FOR VALUES IN (%s)'
            )
        try:
            schema_editor.add_list_partition(
                model=cls,
                name=f"_{unique_value}",
                values=[unique_value],
            )
        except ProgrammingError as e:
            print(f"{cls.__name__}分表失败：" + str(e).rstrip('\n'))
        return


def get_all_models_objects(model_name=None):
    """
    获取所有 models 对象
    :return: {}
    """
    settings.ALL_MODELS_OBJECTS = {}
    if not settings.ALL_MODELS_OBJECTS:
        all_models = apps.get_models()
        for item in list(all_models):
            table = {
                "tableName": item._meta.verbose_name,
                "table": item.__name__,
                "tableFields": []
            }
            for field in item._meta.fields:
                fields = {
                    "title": field.verbose_name,
                    "field": field.name
                }
                table['tableFields'].append(fields)
            settings.ALL_MODELS_OBJECTS.setdefault(item.__name__, {"table": table, "object": item})
    if model_name:
        return settings.ALL_MODELS_OBJECTS[model_name] or {}
    return settings.ALL_MODELS_OBJECTS or {}
