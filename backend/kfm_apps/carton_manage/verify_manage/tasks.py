import os
import zipfile
from shutil import copyfile

import django

from application import settings
from carton_manage.production_manage.models import ProductionWork
from utils.currency import get_back_haul_file_path, des_descrypt_file, get_back_haul_file_des_crypt_path, md5_value

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()
from application.celery import app
from carton_manage.verify_manage.models import BackHaulFile, VerifyCodeRecord
from django_tenants.utils import schema_context


@app.task
def back_haul_file_check(back_haul_file_id):
    """
    回传文件校验
    """
    print(1, back_haul_file_id)
    back_haul_file_obj = BackHaulFile.objects.get(id=back_haul_file_id)
    # 1. 进行DES解密
    file_position = back_haul_file_obj.file_position
    code_package_format_obj = back_haul_file_obj.code_package_format
    file_position_path = os.path.join(get_back_haul_file_path(), file_position)
    file_des_crypt_position = os.path.join(get_back_haul_file_des_crypt_path(), file_position)
    des_crypt_position_path = os.path.join(get_back_haul_file_des_crypt_path(),
                                           file_position.replace(file_position.split(os.sep)[-1], ''))
    if not os.path.exists(des_crypt_position_path):  # 文件夹不存在则创建
        os.makedirs(des_crypt_position_path)
    # 复制文件到专属解密文件夹
    copyfile(file_position_path, file_des_crypt_position)
    des_descrypt_file(file_des_crypt_position, settings.ENCRYPTION_KEY_ID[back_haul_file_obj.key_id])
    # 2. 通过首行校验本包为内码还是外码
    data_dict = {}  # 所有数据的字典
    unrecognized_dict = {}  # 未识别数据
    with zipfile.ZipFile(file_des_crypt_position) as zip_file:
        file_name_list = zip_file.namelist()  # 得到压缩包里所有文件
        for file in file_name_list:
            with zip_file.open(file, 'r') as myfile:  # 得到压缩包里所有文件
                for ele in myfile.readlines():
                    line_data = ele.decode('utf-8').replace('\n' if code_package_format_obj.line_feed == 0 else '\r\n',
                                                            '')
                    code_content = line_data.split(code_package_format_obj.separator)[
                        code_package_format_obj.code_position]
                    ac_time = line_data.split(code_package_format_obj.separator)[code_package_format_obj.time_position]
                    # 2.1 把所有的数据存入一个大字典中
                    if code_content == '000000':
                        data_dict[md5_value(code_content)] = {"code_content": code_content, "ac_time": ac_time}
                    else:
                        unrecognized_dict[code_content] = ac_time  # 未识别数据
                    # 2.2 查询当前码是否存在ck中
                    # 2.3 查询当前生产工单码
                    # error_code_content = ''
                    # error_type = 1
                    # rep_code_id = None
                    # if code_content == '000000':
                    #     error_type = 0
                    #     error_code_content = code_content
                    # verify_code_record_list.append(VerifyCodeRecord(**{
                    #     "production_work_no": production_work_no,
                    #     "back_haul_file": back_haul_file_obj,
                    #     "code_content_md5": md5_value(code_content),
                    #     "error_code_content": error_code_content,
                    #     "code_type": code_type,
                    #     "ac_time": ac_time,
                    #     "error_type": error_type,
                    #     "rep_code_id": rep_code_id
                    # }))
    # 2.2 在ck中查询所有数据
    package_id = back_haul_file_obj.production_work.code_package_id
    ck_verify_code_data = VerifyCodeRecord.ck_verify_code(data=data_dict,package_id=package_id)
    # 3. 保存记录到校验码记录表中
    verify_code_record_list = []
    production_work_no = back_haul_file_obj.production_work.no

    # 3.0 未识别码入库
    for code_content,ac_time in unrecognized_dict.items():
        verify_code_record_list.append(VerifyCodeRecord(**{
            "production_work_no": production_work_no,
            "back_haul_file": back_haul_file_obj,
            "code_content_md5": md5_value(code_content),
            "error_code_content": code_content,
            "code_type": 2,
            "ac_time": ac_time,
            "error_type": 0,
        }))
    # 3.1 正常码入库
    for code_content_md5, value in ck_verify_code_data.get('error_type_1').items():
        code_type = value.get('code_type')
        ac_time = data_dict[code_content_md5].get('ac_time')
        # code_content = data_dict[code_content_md5].get('code_content')
        verify_code_record_list.append(VerifyCodeRecord(**{
            "production_work_no": production_work_no,
            "back_haul_file": back_haul_file_obj,
            "code_content_md5": code_content_md5,
            "code_type": code_type,
            "ac_time": ac_time,
            "error_type": 1,
        }))
    # 3.2 码不存在
    for code_content_md5, value in ck_verify_code_data.get('error_type_2').items():
        code_content = data_dict[code_content_md5].get('code_content')
        ac_time = data_dict[code_content_md5].get('ac_time')
        verify_code_record_list.append(VerifyCodeRecord(**{
            "production_work_no": production_work_no,
            "back_haul_file": back_haul_file_obj,
            "code_content_md5": code_content_md5,
            "error_code_content": code_content,
            "code_type": 2,
            "ac_time": ac_time,
            "error_type": 2,
        }))

    # 3.3 本检测包重码
    for code_content_md5, value in ck_verify_code_data.get('error_type_3').items():
        code_content = data_dict[code_content_md5].get('code_content')
        code_type = value.get('code_type')
        rep_code_id = value.get('rep_code_id')
        ac_time = data_dict[code_content_md5].get('ac_time')
        verify_code_record_list.append(VerifyCodeRecord(**{
            "production_work_no": production_work_no,
            "back_haul_file": back_haul_file_obj,
            "code_content_md5": code_content_md5,
            "error_code_content": code_content,
            "code_type": code_type,
            "ac_time": ac_time,
            "error_type": 3,
        }))

    # 3.4 本生产工单重码
    for code_content_md5, value in ck_verify_code_data.get('error_type_4').items():
        code_content = data_dict[code_content_md5].get('code_content')
        code_type = value.get('code_type')
        rep_code_id = value.get('rep_code_id')
        rep_package_id = value.get('rep_package_id')
        rep_tenant_id = value.get('rep_tenant_id')
        ac_time = data_dict[code_content_md5].get('ac_time')
        verify_code_record_list.append(VerifyCodeRecord(**{
            "production_work_no": production_work_no,
            "back_haul_file": back_haul_file_obj,
            "code_content_md5": code_content_md5,
            "error_code_content": code_content,
            "code_type": code_type,
            "ac_time": ac_time,
            "error_type": 4,
            "rep_code_id": rep_code_id,
            "rep_package_id": rep_package_id,
            "rep_tenant_id": rep_tenant_id,
        }))
    # 3.5 非本生产工单码
    for code_content_md5, value in ck_verify_code_data.get('error_type_5').items():
        code_content = data_dict[code_content_md5].get('code_content')
        code_type = value.get('code_type')
        rep_code_id = value.get('rep_code_id')
        rep_package_id = value.get('rep_package_id')
        rep_tenant_id = value.get('rep_tenant_id')
        ac_time = data_dict[code_content_md5].get('ac_time')
        verify_code_record_list.append(VerifyCodeRecord(**{
            "production_work_no": production_work_no,
            "back_haul_file": back_haul_file_obj,
            "code_content_md5": code_content_md5,
            "error_code_content": code_content,
            "code_type": code_type,
            "ac_time": ac_time,
            "error_type": 5,
            "rep_code_id": rep_code_id,
            "rep_package_id": rep_package_id,
            "rep_tenant_id": rep_tenant_id,
        }))

    VerifyCodeRecord.objects.bulk_create(verify_code_record_list)
    # 4. 更新识别后的结果到回传文件管理表中
    back_haul_file_obj.update_result(back_haul_file_obj.id)



if __name__ == '__main__':
    with schema_context("demo"):
        # from carton_manage.verify_manage.models import VerifyCodeRecord
        # VerifyCodeRecord.add_list_partition('20230206095732408449')
        back_haul_file_check(1)
