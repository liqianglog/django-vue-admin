import datetime
import functools
import os

import django
from django.db import connection

from application import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()
from django_tenants.utils import schema_context

from application.celery import app
from carton_manage.code_manage.models import CodePackage, CodeRepetitionRecord
from utils.currency import des_encrypt_file, zip_compress_file, get_code_package_import_txt_path, md5_file, md5_value
from dvadmin_tenants.models import HistoryTemporaryCode, HistoryCodeInfo, Client


def base_task_error():
    """
    celery 通用装饰器
    :return:
    """

    def wraps(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as exc:
                code_package_obj = CodePackage.objects.get(id=kwargs.get('code_package_id'))
                code_package_obj.write_log({
                    "content": f"未知错误",
                    "remark": f"错误信息:{exc}",
                    "step": 9,
                    "type": 'error'
                })
                raise

        return wrapper

    return wraps


@base_task_error()
@app.task
def code_package_import_check(code_package_id):
    """
    码包导入校验确认(单队列)
    1.校验码包状态
    2.根据规则验证码包是否合格
    3.码包本身重码验证
    4.历史重码校验
    5.数据入库到ck中
    6.对数据进行加密并删除源数据
    code_package_id: 码包ID
    """
    code_package_obj = CodePackage.objects.get(id=code_package_id)
    code_package_obj.import_log = None
    code_package_obj.import_start_datetime = datetime.datetime.now()
    code_package_obj.save()
    # 1.校验码包状态

    if code_package_obj.validate_status not in [1, 2]:
        code_package_obj.write_log({
            "content": f"码包校验状态",
            "remark": f"当前状态为:[{code_package_obj.validate_status}]{code_package_obj.get_validate_status_display()}",
            "step": 1,
            "type": 'error'
        })
        return f"校验状态错误:{code_package_obj.get_validate_status_display()}"
    code_package_obj.validate_status = 2
    code_package_obj.save()
    code_package_obj.write_log({"content": f"码包状态", "step": 1, })
    # 2.根据规则验证码包是否合格
    source_file_path = os.path.join(get_code_package_import_txt_path(), code_package_obj.file_position)
    code_package_template_obj = code_package_obj.code_package_template
    with open(source_file_path) as file:
        readline = file.readline()
        old_readline = readline
        # 2.1.校验换行符
        if (code_package_template_obj.line_feed == 1 and not readline.endswith(
                '\r\n')) or code_package_template_obj.line_feed == 0 and readline.endswith('\r\n'):  # 回车换行
            # 换行符校验失败
            code_package_obj.write_log({
                "content": '规则验证-换行符',
                "remark": old_readline,
                "step": 2.1,
                "type": 'error',
            })
            return "规则验证-换行符校验失败"
        code_package_obj.write_log({"content": f"规则验证-换行符", "step": 2.1})
        # 2.2.校验整体字符长度
        readline = old_readline.replace('\r\n', '').replace('\n', '')
        if len(readline) != code_package_template_obj.char_length:
            code_package_obj.write_log({
                "content": '规则验证-整体字符长度',
                "remark": old_readline,
                "step": 2.2,
                "type": 'error'
            })
            return "规则验证-整体字符长度校验失败"
        code_package_obj.write_log({"content": f"规则验证-整体字符长度", "step": 2.1})
        # 2.3.分隔符
        readline_list = readline.split(code_package_template_obj.separator)
        if len(readline_list) <= 1:
            code_package_obj.write_log({
                "content": '规则验证-分隔符',
                "remark": old_readline,
                "step": 2.3,
                "type": 'error'
            })
            return "规则验证-分隔符校验失败"
        code_package_obj.write_log({"content": f"规则验证-分隔符", "step": 2.3})
        # 2.4.分割后的字段数
        if len(readline_list) != code_package_template_obj.fields:
            code_package_obj.write_log({
                "content": '规则验证-字段数',
                "remark": old_readline,
                "step": 2.4,
                "type": 'error'
            })
            return "规则验证-字段数校验失败"
        code_package_obj.write_log({"content": f"规则验证-字段数", "step": 2.4})
        if code_package_template_obj.code_type in [0, 2]:  # 外码
            # 2.5.外码内容长度
            if len(readline_list[-1]) != code_package_template_obj.w_url_length:
                code_package_obj.write_log({
                    "content": '规则验证-外码内容长度',
                    "remark": old_readline,
                    "step": 2.5,
                    "type": 'error'
                })
                return "规则验证-外码内容长度校验失败"
            code_package_obj.write_log({"content": f"规则验证-外码内容长度", "step": 2.5})
        if code_package_template_obj.code_type in [1, 2]:  # 内码
            # 2.6.内码内容长度
            if len(readline_list[-1]) != code_package_template_obj.n_url_length:
                code_package_obj.write_log({
                    "content": '规则验证-内码内容长度',
                    "remark": old_readline,
                    "step": 2.6,
                    "type": 'error'
                })
                return "规则验证-内码内容长度校验失败"
            code_package_obj.write_log({"content": f"规则验证-内码内容长度", "step": 2.6})
        # 2.7.外码网址校验
        if code_package_template_obj.code_type in [0, 2]:  # 外码
            w_url = readline_list[code_package_template_obj.w_field_position]
            if not w_url.startswith(code_package_template_obj.w_url_prefix):
                code_package_obj.write_log({
                    "content": '规则验证-外码网址',
                    "remark": old_readline,
                    "step": 2.7,
                    "type": 'error'
                })
                return "规则验证-外码网址校验失败"
            code_package_obj.write_log({"content": f"规则验证-外码网址", "step": 2.7})
        # 2.8.内码网址校验
        if code_package_template_obj.code_type in [1, 2]:  # 内码
            n_url = readline_list[code_package_template_obj.n_field_position]
            if not n_url.startswith(code_package_template_obj.n_url_prefix):
                code_package_obj.write_log({
                    "content": '规则验证-内码网址',
                    "remark": old_readline,
                    "step": 2.8,
                    "type": 'error'
                })
                return "规则验证-内码网址校验失败"
            code_package_obj.write_log({"content": f"规则验证-内码网址", "step": 2.8})
    code_data_list = []
    # 码数据先入临时表中
    _HistoryTemporaryCode = HistoryTemporaryCode.set_db(timeout=60 * 30)
    _HistoryTemporaryCode.create_table(table_suffix=code_package_obj.id)
    tenant_id = Client.objects.get(schema_name=connection.tenant.schema_name).id
    with open(source_file_path) as file:
        for readline in file:
            readline = readline.replace('\r\n', '').replace('\n', '')
            readline_list = readline.split(code_package_template_obj.separator)
            if code_package_template_obj.code_type in [0, 2]:  # 外码
                w_url = readline_list[code_package_template_obj.w_field_position]
                code_data_list.append(_HistoryTemporaryCode(
                    code=md5_value(w_url),
                    code_type='1',
                    content=w_url,
                    tenant_id=f"{tenant_id}",
                    package_id=f"{code_package_obj.id}",
                    timestamp=datetime.datetime.now()
                ))
            if code_package_template_obj.code_type in [1, 2]:  # 内码
                n_url = readline_list[code_package_template_obj.n_field_position]
                code_data_list.append(_HistoryTemporaryCode(
                    code=md5_value(n_url),
                    code_type='0',
                    content=n_url,
                    tenant_id=f"{tenant_id}",
                    package_id=f"{code_package_obj.id}",
                    timestamp=datetime.datetime.now()
                ))
            if len(code_data_list) >= 500000:
                _HistoryTemporaryCode.bulk_insert(code_data_list)
                code_data_list = []
    if len(code_data_list) != 0:
        _HistoryTemporaryCode.bulk_insert(code_data_list)
    # 3.码包本身重码验证
    count, data = _HistoryTemporaryCode.select_duplicate()
    if count != 0:
        # 问题码入库
        error_data_list = []
        for key, val in data.items():
            for ele in range(val.get('count') - 1):
                error_data_list.append(CodeRepetitionRecord(
                    **{
                        "code_package": code_package_obj,
                        "repetition_code_package": code_package_obj,
                        "code_content": val.get('content'),
                        "code_content_md5": key,
                        "code_type": val.get('code_type'),
                        "repetition_type": 0,
                        "creator": code_package_obj.creator,
                        "modifier": code_package_obj.modifier,
                        "dept_belong_id": code_package_obj.dept_belong_id,
                    }
                ))
        CodeRepetitionRecord.objects.bulk_create(error_data_list)
        _HistoryTemporaryCode.delete()
        code_package_obj.write_log({
            "content": f'本码包查重',
            "remark": f"发现重码数{len(error_data_list)}个",
            "step": 3,
            "type": 'error'
        })
        return
    code_package_obj.write_log({"content": '本码包查重', "step": 3})
    # 4.历史重码校验
    from_table = HistoryCodeInfo.get_base_all_model().table_name()
    _HistoryCodeInfo = HistoryCodeInfo.set_db()
    count, history_code_data = _HistoryTemporaryCode.verify_history_code_repetition(
        from_db=_HistoryCodeInfo.db.db_name, from_table=from_table)
    if count != 0:
        if count > 1000:
            code_package_obj.write_log({
                "content": '历史查重',
                "remark": '历史码数据中发现大量重复码,重复数量超过1000,请检查码包是否重复导入!',
                "step": 4,
                "type": 'error'
            })
            _HistoryTemporaryCode.delete()
            return
        duplicate_list = []
        for key, val in history_code_data.items():
            # 获取明码内容
            duplicate_list.append(CodeRepetitionRecord(
                **{
                    "code_package": code_package_obj,
                    "repetition_code_package_id": val.get('repetition_code_package'),
                    "code_content": val.get('content'),
                    "code_content_md5": key,
                    "code_type": val.get('code_type'),
                    "repetition_type": 1,
                    "creator": code_package_obj.creator,
                    "modifier": code_package_obj.modifier,
                    "dept_belong_id": code_package_obj.dept_belong_id,
                }
            ))
        CodeRepetitionRecord.objects.bulk_create(duplicate_list)
        _HistoryTemporaryCode.delete()
        code_package_obj.write_log({
            "content": f'历史查重',
            "remark": f'历史码包重复码校验失败，发现重码数{len(duplicate_list)}个',
            "step": 4,
            "type": 'error'
        })
        return
    code_package_obj.write_log({"content": '历史查重', "step": 4})
    # 5.数据入库到ck中
    _HistoryTemporaryCode.insert_history(from_table, insert_db=HistoryCodeInfo.db.db_name)
    _HistoryTemporaryCode.delete()
    # 6.对数据进行加密并删除源数据
    target_file_path = source_file_path.replace('.txt', '.zip')
    zip_compress_file(source_file_path, target_file_path, is_rm=True)
    des_encrypt_file(target_file_path, settings.ENCRYPTION_KEY_ID[code_package_obj.key_id])
    os.rename(target_file_path, target_file_path.replace('.zip', '.zip.des'))
    code_package_obj = CodePackage.objects.get(id=code_package_id)
    code_package_obj.file_position = code_package_obj.file_position.replace('.txt', '.zip.des')
    code_package_obj.validate_status = 4
    code_package_obj.des_file_md5 = md5_file(
        os.path.join(get_code_package_import_txt_path(), code_package_obj.file_position))
    code_package_obj.save()
    code_package_obj.write_log({"content": '全部校验', "step": 5})


if __name__ == '__main__':
    with schema_context("demo"):
        HistoryCodeInfo.set_db().create_table()
        code_package_import_check([2])
        # print(json.loads(CodePackage.objects.get(id=2).import_log))
