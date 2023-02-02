import os
import time
import uuid
from datetime import datetime

import django
from infi.clickhouse_orm import DateTimeField, StringField, ReplacingMergeTree, Memory

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()
from click_house.models import ClusterModel


class CodeInfo(ClusterModel):
    code = StringField()
    values = StringField()
    timestamp = DateTimeField()
    engine = ReplacingMergeTree('timestamp', ('code',),
                                replica_table_path='/clickhouse/tables/{database}/{table}/{shard}',
                                replica_name='{replica}')

    @classmethod
    def table_name(cls):
        return "code_info_test"


class TemporaryCode(ClusterModel):
    code = StringField()
    values = StringField()
    timestamp = DateTimeField()
    engine = ReplacingMergeTree('timestamp', ('code',),
                                replica_table_path='/clickhouse/tables/{database}/{table}/{shard}',
                                replica_name='{replica}')

    @classmethod
    def table_name(cls):
        return "temporary_code1"


if __name__ == '__main__':

    # 1. 创建表
    # print(CodeInfo.create_table_sql())
    # print(CodeInfo.create_all_table_sql())
    # print(CodeInfo.create_table())
    # # 2. 查询总数
    # print(CodeInfo().objects.count())
    # # 3. 批量插入数据
    # data = []
    # for _ in range(1):
    #     t1 = time.time()
    #     for i in range(100000):
    #         data.append(CodeInfo(code=uuid.uuid4().hex, values="1:10", timestamp=datetime.now()))
    #     count = CodeInfo.bulk_insert(data)
    #     print(f"总共插入:{count} 条")
    #     # print(f"现库中数据量:{CodeInfo().objects.count()}条")
    #     print(f"插入数据总耗时:{time.time() - t1}")
    # 4. 查重数据
    # count, data = CodeInfo.select_duplicate(where="values='1:10'")
    # 5. 创建临时表
    print(TemporaryCode.set_db('10'))
    # print(TemporaryCode.create_table_sql())
    print(TemporaryCode.create_table())
    # print(TemporaryCode.create_all_table_sql())
    # print(TemporaryCode.delete())
    # print(TemporaryCode.exists())
    # # print(TemporaryCode.create_all_table_sql())
    # # print(TemporaryCode.create_table_sql())
    # print(TemporaryCode.create_table())
    # print(TemporaryCode.objects.count())

    # # # print(CodeInfo().objects.filter(code="0000e159c1f4451ea65814744c264e37").count())
    # # # 6. 批量插入临时表
    # #

    data = []
    sum = 1
    t0 = time.time()
    t1 = 0
    t2 = 0
    max_time = 0
    for _ in range(sum):
        time1 = time.time()
        for i in range(10000):
            data.append(TemporaryCode(code=uuid.uuid4().hex, values=uuid.uuid4().hex, timestamp=datetime.now()))
        _t1 = time.time() - time1
        # print(f"实例化耗时:{round(_t1, 2)}")
        t1 += _t1

        time2 = time.time()
        count = TemporaryCode.set_db('10').bulk_insert(data)
        # print(f"总共插入:{count} 条")

        _t2 = time.time() - time2
        if _t2 > max_time:
            max_time = _t2
        t2 += _t2
        # print(f"插入数据耗时:{round(_t2, 2)}")
        # print(f"插入总耗时:{round(_t1 + _t2, 2)}")
        data = []
    #
    print(f"现库中数据量:{TemporaryCode.set_db('10').objects.count()}条")
    print(f"实例化,总耗时:{t1},平均耗时:{t1 / sum}")
    print(f"插入总耗时:{t2},平均耗时:{t2 / sum}")
    print(f"总耗时:{int(time.time() - t0)},总平均耗时:{int(time.time() - t0) / sum}")
    print(f"插入数据最长耗时:{int(max_time)}")
