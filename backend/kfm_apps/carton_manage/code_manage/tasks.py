import os

import django

from application import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()
from django_tenants.utils import schema_context

from application.celery import app
from carton_manage.code_manage.models import CodePackage
from utils.currency import des_encrypt_file, zip_compress_file, get_code_package_import_txt_path, md5_file, read_max_row


@app.task
def code_package_import_check(code_package_ids):
    """
    码包导入校验确认
    1.校验码包状态
    2.根据规则验证码包是否合格
    3.码包本身重码验证
    4.历史重码校验
    5.数据入库到ck中
    6.对数据进行加密并删除源数据
    code_package_id: 码包ID
    """
    for code_package_id in code_package_ids:
        code_package_obj = CodePackage.objects.get(id=code_package_id)
        # 1.校验码包状态
        if code_package_obj.validate_status != 1:
            return f"校验状态错误:{code_package_obj.get_validate_status_display()}"
        file_path = os.path.join(get_code_package_import_txt_path(), code_package_obj.file_position)
        total_number = read_max_row(file_path).get('count')  # 文件总行数
        file_md5 = md5_file(file_path)  # 文件MD5 值
        code_package_obj.total_number = total_number
        code_package_obj.file_md5 = file_md5
        code_package_obj.validate_status = 2
        code_package_obj.save()
        # 2.根据规则验证码包是否合格
        # 3.码包本身重码验证
        # 4.历史重码校验
        # 5.数据入库到ck中
        # 6.对数据进行加密并删除源数据
        source_file_path = os.path.join(get_code_package_import_txt_path(), code_package_obj.file_position)
        target_file_path = source_file_path.replace('.txt', '.zip')
        zip_compress_file(source_file_path, target_file_path, is_rm=True)
        des_encrypt_file(target_file_path, settings.ENCRYPTION_KEY_ID[code_package_obj.key_id])
        os.rename(target_file_path, target_file_path.replace('.zip', '.zip.des'))
        code_package_obj.file_position = code_package_obj.file_position.replace('.txt', '.zip.des')
        code_package_obj.validate_status = 4
        code_package_obj.des_file_md5 = md5_file(
            os.path.join(get_code_package_import_txt_path(), code_package_obj.file_position))
        code_package_obj.save()


if __name__ == '__main__':
    with schema_context("demo"):
        code_package_import_check(1)
