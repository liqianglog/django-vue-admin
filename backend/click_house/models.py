import logging
import re

from django.conf import settings
from infi.clickhouse_orm import Model, Distributed, DistributedModel, QuerySet

from .db_pool import get_click_house_pool

logger = logging.getLogger(__name__)


class ClusterBaseModel(object):
    db = None
    objects: QuerySet = None

    @classmethod
    def set_db(cls, brand_owner_id, timeout=120):
        cls.db = get_click_house_pool(brand_owner_id, timeout=timeout)
        cls.objects = QuerySet(
            cls.get_base_all_model() if hasattr(cls, 'get_base_all_model') else cls,
            cls.db)
        return cls


class ClusterDistributedModel(DistributedModel, ClusterBaseModel):
    """
    分布式Model
    """
    _table_name = None

    @classmethod
    def create_table_sql(cls, db=None):
        if not db:
            db = cls.db
        assert isinstance(cls.engine, Distributed), "engine must be engines.Distributed instance"
        cls.fix_engine_table()
        parts = [
            'CREATE TABLE IF NOT EXISTS `{0}`.`{1}` ON CLUSTER {3} AS `{0}`.`{2}`'.format(
                db.db_name, cls.table_name(), cls.engine.table_name, settings.CLICK_HOUSE_CLUSTER_NAME),
            'ENGINE = ' + cls.engine.create_table_sql(db)]
        return '\n'.join(parts)

    @classmethod
    def table_name(cls):
        if cls._table_name:
            return cls._table_name
        return re.sub('(?<!^)(?=[A-Z])', '_', cls.__name__).lower()

    @classmethod
    def create_table(cls):
        return cls.db.create_table(cls)


class ClusterModel(Model, ClusterBaseModel):
    """
    基础 Model
    """
    _table_model = None
    _table_name = None

    @classmethod
    def get_base_all_model(cls):
        """
        获取BaseAll模型
        """
        if cls._table_model:
            return cls._table_model

        class ClusterModelAll(ClusterDistributedModel, cls):
            inherit_cls = cls
            engine = Distributed(settings.CLICK_HOUSE_CLUSTER_NAME, inherit_cls, 'rand()')

            @classmethod
            def table_name(cls):
                return f"{cls.inherit_cls.table_name()}_all"

        cls._table_model = ClusterModelAll
        return cls._table_model

    @classmethod
    def create_table_sql(cls, db=None):
        '''
        Returns the SQL statement for creating a table for this model.
        '''
        if not db:
            db = cls.db
        parts = ['CREATE TABLE IF NOT EXISTS `%s`.`%s` ON CLUSTER `%s`  (' % (
            db.db_name, cls.table_name(), settings.CLICK_HOUSE_CLUSTER_NAME)]
        # Fields
        items = []
        for name, field in cls.fields().items():
            items.append('    %s %s' % (name, field.get_sql(db=db)))
        # Constraints
        for c in cls._constraints.values():
            items.append('    %s' % c.create_table_sql())
        # Indexes
        for i in cls._indexes.values():
            items.append('    %s' % i.create_table_sql())
        parts.append(',\n'.join(items))
        # Engine
        parts.append(')')
        parts.append('ENGINE = ' + cls.engine.create_table_sql(db))
        return '\n'.join(parts)

    @classmethod
    def table_name(cls):
        if cls._table_name:
            return cls._table_name
        return re.sub('(?<!^)(?=[A-Z])', '_', cls.__name__).lower()

    @classmethod
    def set_table_name(cls, name):
        cls._table_name = name
        return cls

    @classmethod
    def create_all_table_sql(cls):
        return cls.get_base_all_model().create_table_sql()

    @classmethod
    def create_table(cls):
        # 创建基础表
        cls.db.create_table(cls)
        # 创建分布式表
        cls.get_base_all_model().create_table()
        return True

    @classmethod
    def bulk_insert(cls, data: list):
        """
        批量创建数据
        :param data:
        :return:
        """
        cls.db.insert(data)
        return len(data)

    @classmethod
    def select_duplicate(cls, limit=1000, where=""):
        """
        本表内查重
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
        order_by = cls.engine.order_by[0]
        sql = f"""SELECT
            {order_by},count() AS cnt
        FROM {cls.db.db_name}.{cls.get_base_all_model().table_name()}
        {f'WHERE {where}' if where else ""}
        GROUP BY {order_by}
        HAVING cnt > 1
        ORDER BY {order_by} ASC  limit {limit}
        """
        result_data = {}
        logger.debug("码包本身是否有重复开始...")
        result = cls.db.raw(sql)
        logger.debug(sql)
        # 获取所有重码
        for ele in result.split('\n'):
            if ele:
                result_data[ele.split('\t')[0]] = {"values": "", "content": "", "count": int(ele.split('\t')[1])}
        if result_data:
            # 获取重码详细内容
            sql = f"""
SELECT {order_by},values,content FROM {cls.db.db_name}.{cls.get_base_all_model().table_name()} 
WHERE {order_by}  GLOBAL IN {list(result_data.keys())}
"""
            logger.debug(sql)
            result = cls.db.raw(sql)
            for ele in result.split('\n'):
                if ele:
                    result_data[ele.split('\t')[0]]["values"] = ele.split('\t')[1]
                    result_data[ele.split('\t')[0]]["content"] = ele.split('\t')[2]
        logger.debug("码包本身是否有重复结束...")
        return len(result_data.keys()), result_data

    @classmethod
    def verify_history_code_repetition(cls, from_table=""):
        """
        历史码内查重
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
        order_by = cls.engine.order_by[0]
        sql = f"""
SELECT {order_by},count() FROM {cls.db.db_name}.{from_table} 
WHERE {order_by} GLOBAL IN (
    SELECT {order_by} FROM {cls.db.db_name}.{cls.get_base_all_model().table_name()}
) 
group by {order_by} limit 1001
        """
        result_data = {}
        logger.debug("匹配历史码开始...")
        logger.debug(sql)
        result = cls.db.raw(sql)
        repetition_count = 0
        for ele in result.split('\n'):
            if ele:
                repetition_count += int(ele.split('\t')[1])
                result_data[ele.split('\t')[0]] = {"values": "", "content": "", "count": int(ele.split('\t')[1])}
        if result_data:
            # 获取重码详细内容
            sql = f"""
SELECT {order_by},values,content FROM {cls.db.db_name}.{cls.get_base_all_model().table_name()} 
WHERE {order_by}  GLOBAL IN {list(result_data.keys())}
"""
            logger.debug(sql)
            result = cls.db.raw(sql)
            for ele in result.split('\n'):
                if ele:
                    result_data[ele.split('\t')[0]]["values"] = ele.split('\t')[1]
                    result_data[ele.split('\t')[0]]["content"] = ele.split('\t')[2]
        logger.debug("匹配历史码结束...")
        return repetition_count, result_data

    @classmethod
    def exists(cls):
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
        sql = f"""EXISTS {cls.db.db_name}.{cls.table_name()}"""
        return True if cls.db.raw(sql).strip('\n|\t') == '1' else False

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
        exists = cls.exists()
        sql = f"""DROP TABLE IF EXISTS {cls.db.db_name}.{cls.table_name()} ON CLUSTER {settings.CLICK_HOUSE_CLUSTER_NAME}"""
        cls.db.raw(sql)
        sql = f"""DROP TABLE IF EXISTS {cls.db.db_name}.{cls.table_name()}_all ON CLUSTER {settings.CLICK_HOUSE_CLUSTER_NAME}"""
        cls.db.raw(sql)
        return exists
