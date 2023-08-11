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
from django.db import models, transaction, connection, ProgrammingError
from django.core.exceptions import ObjectDoesNotExist

from application import settings
from application.dispatch import is_tenants_mode

table_prefix = settings.TABLE_PREFIX  # 数据库表名前缀


class SoftDeleteQuerySet(models.query.QuerySet):
    @transaction.atomic
    def delete(self, cascade=True):
        if cascade:  # delete one by one if cascade
            for obj in self.all():
                obj.delete(cascade=cascade)
        return self.update(is_deleted=True)

    def hard_delete(self):
        return super().delete()


class SoftDeleteManager(models.Manager):
    """支持软删除"""

    def __init__(self, *args, **kwargs):
        self.__add_is_del_filter = False
        super(SoftDeleteManager, self).__init__(*args, **kwargs)

    def filter(self, *args, **kwargs):
        # 考虑是否主动传入is_deleted
        if not kwargs.get("is_deleted") is None:
            self.__add_is_del_filter = kwargs.get("is_deleted")
        return super(SoftDeleteManager, self).filter(*args, **kwargs)

    def get_queryset(self):
        if self.__add_is_del_filter:
            return SoftDeleteQuerySet(self.model, using=self._db).exclude(is_deleted=False)
        return SoftDeleteQuerySet(self.model).exclude(is_deleted=True)

    def get_by_natural_key(self, name):
        return SoftDeleteQuerySet(self.model).get(username=name)


def get_month_range(start_day, end_day):
    months = (end_day.year - start_day.year) * 12 + end_day.month - start_day.month
    month_range = [
        "%s-%s-01" % (start_day.year + mon // 12, str(mon % 12 + 1).zfill(2))
        for mon in range(start_day.month - 1, start_day.month + months)
    ]
    return month_range


class SoftDeleteModel(models.Model):
    """
    软删除模型
    一旦继承,就将开启软删除
    """

    is_deleted = models.BooleanField(verbose_name="是否软删除", help_text="是否软删除", default=False, db_index=True)
    objects = SoftDeleteManager()

    class Meta:
        abstract = True
        verbose_name = "软删除模型"
        verbose_name_plural = verbose_name

    @transaction.atomic
    def delete(self, using=None, cascade=True, *args, **kwargs):
        """
        重写删除方法,直接开启软删除
        """
        self.is_deleted = True
        self.save(using=using)
        if cascade:
            self.delete_related_objects(raise_exception=True)
        # raise Exception("delete_related_objects")

    def hard_delete(self):
        return super().delete()

    soft_delete_kwargs = {
        "related_names": [],
    }

    @classmethod
    def _get_kwargs(cls):
        return cls.soft_delete_kwargs

    @classmethod
    def _get_relations(cls):
        relations = {"foreign": [], "self": []}
        related_fields = cls._get_kwargs().get("related_names", [])
        if not related_fields:
            fields = cls._meta.get_fields(include_hidden=True)
            mutated_fields = [field for field in fields if field.is_relation and hasattr(field, "related_name")]
            m2m_models = [field.through for field in mutated_fields if field.many_to_many]
            related_fields = [
                field.related_name
                for field in mutated_fields
                if not field.many_to_many and field.related_model not in m2m_models and field.related_name
            ]
            tree_model_field = [
                field.field.name
                for field in mutated_fields
                if not field.many_to_many and field.related_model is field.model
            ]
            relations["self"] = f"{tree_model_field[0]}_id" if len(tree_model_field) == 1 else None
        relations["foreign"] = related_fields
        return relations

    def _is_cascade(self, relation):
        on_delete_case = self._meta.get_field(relation).on_delete.__name__
        return on_delete_case == "CASCADE"

    def _get_related_objects(self, relation):
        qs = getattr(self, relation)
        if isinstance(qs, models.Manager):
            return qs
        return

    def related_objects(self, raise_exception=False, use_soft_manager=False):
        relations = self._get_relations()
        objects = {}
        for relation in relations["foreign"]:
            try:
                qs = self._get_related_objects(relation)
            except ObjectDoesNotExist as e:
                if raise_exception:
                    raise e
                continue
            else:
                objects[relation] = qs
        if relations["self"]:
            objects["self"] = self.__class__.objects.filter(**{relations["self"]: self.id})
        print(f"related_objects: {objects}", flush=True)
        return objects

    def delete_related_objects(self, raise_exception=False):
        for relation, qs in self.related_objects(raise_exception=raise_exception).items():
            if relation == "self":
                qs.delete()
                continue
            if self._is_cascade(relation):
                print(f"model {self.__class__} : cascade delete {relation} objects {qs.all()}", flush=True)
                qs.all().delete()
            else:
                print(f"model {self.__class__} : protect delete {relation} objects {qs.all()}", flush=True)
                if qs.all().exists():
                    self.hard_delete()
                qs.all().hard_delete()
        # raise Exception("xxxxxxxxxxx for test xxxxxxxxxxx")


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
