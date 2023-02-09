import datetime

from django.db import models, connection
from django_tenants.models import TenantMixin, DomainMixin
from infi.clickhouse_orm import StringField, DateTimeField, MergeTree, QuerySet

from application import dispatch
from click_house.db_pool import get_click_house_pool
from click_house.models import ClusterModel
from dvadmin.utils.models import table_prefix


# 商城微信小程序


def auth_id():
    client = Client.objects.all().order_by('-id').values('id').first()
    return client.get('id', 100000) + 1


class Client(TenantMixin):
    id = models.BigAutoField(primary_key=True, help_text="Id", verbose_name="Id", default=auth_id)
    name = models.CharField(max_length=100, help_text="租户名称", verbose_name="租户名称", )
    on_trial = models.BooleanField(help_text="是否启用", verbose_name="是否启用")
    start_datetime = models.DateField(default=datetime.datetime.now, verbose_name="租户有效开始时间",
                                      help_text="租户有效开始时间")
    paid_until = models.DateField(help_text="租户有效截止时间", verbose_name="租户有效截止时间", )
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


class HistoryCodeInfo(ClusterModel):
    """
    历史码数据表
    """
    code = StringField()
    code_type = StringField()  # 0 内码; 1 外码
    tenant_id = StringField()  # 租户id
    package_id = StringField()  # 码包id
    timestamp = DateTimeField()
    engine = MergeTree('timestamp', ('code',),
                       replica_table_path='/clickhouse/tables/{database}/{table}/{shard}',
                       replica_name='{replica}')

    @classmethod
    def set_db(cls, db_name='base', timeout=1200):
        cls.db = get_click_house_pool(db_name, timeout=timeout)
        cls.objects = QuerySet(
            cls.get_base_all_model() if hasattr(cls, 'get_base_all_model') else cls,
            cls.db)
        return cls

    @classmethod
    def delete(cls):
        """
        SELECT
        order_by,count(code) AS cnt
        FROM code_db.code_info_test_all
        GROUP BY code
        HAVING cnt > 1
        ORDER BY code ASC  limit 10000

        :param limit:
        :param where:
        :return: count,data
        """
        raise "本表不支持手动删除"
        exists = cls.exists()
        sql = f"""DROP TABLE IF EXISTS {cls.db.db_name}.{cls.table_name()} ON CLUSTER {settings.CLICK_HOUSE_CLUSTER_NAME}"""
        cls.db.raw(sql)
        sql = f"""DROP TABLE IF EXISTS {cls.db.db_name}.{cls.table_name()}_all ON CLUSTER {settings.CLICK_HOUSE_CLUSTER_NAME}"""
        cls.db.raw(sql)
        return exists

    @classmethod
    def select_data_duplicate(cls, code_list: list, package_id):
        """
        查询数据是否在本工单中
        SELECT
        code,code_type,tenant_id,package_id,content
        FROM code_db.code_info_test_all
        WHERE code IN (code_list) AND tenant_id=tenant_id AND package_id=package_id

        :param code_list:
        :param package_id:
        :return:
        """
        tenant_id = Client.objects.get(schema_name=connection.tenant.schema_name).id
        order_by = cls.engine.order_by[0]
        sql = f"""SELECT
        code,code_type,tenant_id,package_id
        FROM {cls.db.db_name}.{cls.get_base_all_model().table_name()}
        WHERE code IN {code_list} AND tenant_id='{str(tenant_id)}' AND package_id='{str(package_id)}'
        ORDER BY {order_by} ASC
        """
        result_data = {}
        result = cls.db.raw(sql)
        # 获取所有数据
        for ele in result.split('\n'):
            if ele:
                result_data[ele.split('\t')[0]] = {
                    "code_type": ele.split('\t')[1],
                    "tenant_id": ele.split('\t')[2],
                    "package_id": ele.split('\t')[3],
                }
        return result_data
    def select_data_all(cls, code_list: list):
        """
        全表查询码是否存在
        SELECT
        code,code_type,tenant_id,package_id,content
        FROM code_db.code_info_test_all
        WHERE code IN (code_list)

        :param code_list:
        :return:
        """
        order_by = cls.engine.order_by[0]
        sql = f"""SELECT
        code,code_type,tenant_id,package_id
        FROM {cls.db.db_name}.{cls.get_base_all_model().table_name()}
        WHERE code IN {code_list}'
        ORDER BY {order_by} ASC
        """
        result_data = {}
        result = cls.db.raw(sql)
        # 获取所有数据
        for ele in result.split('\n'):
            if ele:
                result_data[ele.split('\t')[0]] = {
                    "code_type": ele.split('\t')[1],
                    "tenant_id": ele.split('\t')[2],
                    "package_id": ele.split('\t')[3],
                }
        return result_data


class HistoryTemporaryCode(ClusterModel):
    """
    临时历史码码数据表
    """
    code = StringField()
    code_type = StringField()  # 0 内码; 1 外码
    tenant_id = StringField()  # 租户id
    package_id = StringField()  # 码包id
    content = StringField()  # 明码内容
    timestamp = DateTimeField()
    engine = MergeTree('timestamp', ('code',),
                       replica_table_path='/clickhouse/tables/{database}/{table}/{shard}',
                       replica_name='{replica}')

    @classmethod
    def set_db(cls, db_name='', timeout=120):
        if not db_name:
            db_name = connection.tenant.schema_name
        return super().set_db(db_name, timeout)

    @classmethod
    def insert_history(cls, insert_table, insert_db=None):
        """
        把临时数据插入历史码数据中
        :param insert_table:
        :return:
        """
        if not insert_db:
            insert_db = cls.db.db_name
        sql = f"""
INSERT INTO {insert_db}.{insert_table}  (code, code_type, tenant_id, package_id, timestamp) 
SELECT code, code_type, tenant_id, package_id, timestamp FROM 
{cls.db.db_name}.{cls.get_base_all_model().table_name()};
        """
        cls.db.raw(sql)
