"""
通用方法封装
"""
import os
import subprocess
import zipfile
from hashlib import md5

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
from django.conf import settings

from application.settings import BASE_DIR


def file_iterator(file_path, start_pos, chunk_size):
    """
    文件生成器，防止文件过大，导致内存溢出
    :param file_path: 文件绝对路径
    :param start_pos: 文件读取的起始位置
    :param chunk_size: 文件读取的块大小
    :return: yield
    """
    with open(file_path, mode='rb') as f:
        f.seek(start_pos, os.SEEK_SET)
        content = f.read(chunk_size)
        yield content


def md5_file(file):
    """
    对文件进行MD5加密
    """

    def file_iterator(file_path, chunck_size=1024):
        """
        文件生成器,防止文件过大，导致内存溢出
        :param file_path: 文件绝对路径
        :param chunk_size: 块大小
        :return: 生成器
        """
        with open(file_path, "rb") as file:
            while True:
                chuck_stream = file.read(chunck_size)
                if chuck_stream:
                    yield chuck_stream
                else:
                    break

    m = md5()
    for file in file_iterator(file):
        m.update(file)
    return m.hexdigest()


def md5_value(value):
    """
    对某个值加密
    """
    m = md5()
    m.update(value.encode(encoding='UTF-8'))
    return m.hexdigest()


def read_max_row(file_path):
    """
    获取文件最大行数
    """
    file = open(file_path, 'r')
    count = 0
    first = None
    for index, line in enumerate(file):
        count += 1
        if index == 0:
            first = line.split(",")[0]
    file.close()
    return {"count": count, "first_line": first}


def read_file_first(file_path):
    """
    读取文件第一行
    """
    with open(file_path) as f:
        # 读取文件第一行
        index = 0
        for line in f:
            if line:
                if index == 0:
                    return line
    return None


def zip_is_txt(zip_list):
    """
    判断码包ZIP中是否全是TXT文件
    """
    txt_count = 0
    for i, f in enumerate(zip_list):
        file_split = os.path.splitext(f)
        if file_split[1] == ".txt":
            txt_count += 1
        else:
            txt_count = 0
    return len(zip_list) == txt_count


def now_datetime():
    """
    获取当前时间
    :return:
    """
    from django.utils import timezone
    now = timezone.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def file_now_datetime():
    """
    获取文件目录当前时间
    :return:
    """
    from django.utils import timezone
    now = timezone.now()
    return now.strftime("%Y%m%d")


def zip_compress_file(source_file_path, target_file_path, is_rm=False):
    """
    压缩文件为zip文件
    :param source_file_path: 源文件
    :param target_file_path: 目标文件
    :param files_path: 文件目录
    :return:
    """
    if not isinstance(source_file_path, list):
        source_file_path = [source_file_path]
    if settings.ENVIRONMENT == 'prod':
        if is_rm:
            cmd = ['zip', '-9jrqm', '-b', '/tmp', target_file_path] + [ele for ele in source_file_path]
        else:
            # 单文件
            cmd = ['zip', '-9jrq', '-b', '/tmp', target_file_path] + [ele for ele in source_file_path]
        p = subprocess.Popen(cmd)
        p.wait()
        return
    with zipfile.ZipFile(target_file_path, 'w', zipfile.ZIP_DEFLATED) as f:
        for ele in source_file_path:
            arcname = ele.split(os.path.sep)[-1]
            f.write(ele, arcname=arcname)
    if is_rm:
        for ele in source_file_path:
            os.remove(ele)


def unzip_compress_file(source_file_path, target_file_path, is_rm=False, pwd=None, specify_file_name=[]):
    """
    解压文件为zip文件
    :param source_file_path: 源文件
    :param target_file_path: 目标文件夹
    :param is_rm: 是否删除
    :param pwd: 解压密码
    :param specify_file_name: 需要解密指定的文件名
    :return:
    """
    if settings.ENVIRONMENT == 'prod':
        if pwd:
            cmd = ['unzip', '-n', '-P', pwd, '-d', target_file_path, source_file_path]
        else:
            cmd = ['unzip', '-n', '-d', target_file_path, source_file_path]
        if specify_file_name:
            cmd += [ele for ele in specify_file_name]
        p = subprocess.Popen(cmd)
        p.wait()
        print(cmd)
        if is_rm:
            os.remove(source_file_path)
        return True
    with zipfile.ZipFile(source_file_path) as zip_file:
        file_name_list = zip_file.namelist()  # 得到压缩包里所有文件
        if specify_file_name:
            file_name_list = [ele for ele in file_name_list if ele in specify_file_name]
        for f in file_name_list:
            zip_file.extract(f, target_file_path, pwd=pwd)

    if is_rm:
        os.remove(source_file_path)
    return True


def get_code_package_import_zip_path():
    """
    码包订单导入zip文件路径
    :return:
    """
    from django.db import connection
    path = os.path.join(BASE_DIR, 'kfm_code_file', 'code_package_zip_file', connection.tenant.schema_name)
    if not os.path.exists(path):  # 文件夹不存在则创建
        os.makedirs(path)
    return path


def get_code_package_import_txt_path():
    """
    码包订单导入txt文件路径
    :return:
    """
    from django.db import connection
    path = os.path.join(BASE_DIR, 'kfm_code_file', 'code_package_txt_file', connection.tenant.schema_name)
    if not os.path.exists(path):  # 文件夹不存在则创建
        os.makedirs(path)
    return path

def get_code_package_import_fail_path():
    """
    码包订单导入失败文件路径
    :return:
    """
    from django.db import connection
    path = os.path.join(BASE_DIR, 'kfm_code_file', 'code_package_fail_file', connection.tenant.schema_name)
    if not os.path.exists(path):  # 文件夹不存在则创建
        os.makedirs(path)
    return path

def get_back_haul_file_path():
    """
    获取回传文件路径
    :return:
    """
    from django.db import connection
    path = os.path.join(BASE_DIR, 'kfm_code_file', 'back_haul_file', connection.tenant.schema_name)
    if not os.path.exists(path):  # 文件夹不存在则创建
        os.makedirs(path)
    return path
def get_back_haul_file_des_crypt_path():
    """
    获取回传文件加密后路径
    :return:
    """
    from django.db import connection
    path = os.path.join(BASE_DIR, 'kfm_code_file', 'back_haul_file_descrypt', connection.tenant.schema_name)
    if not os.path.exists(path):  # 文件夹不存在则创建
        os.makedirs(path)
    return path


def check_zip_is_encrypted(file: str) -> bool:
    '''
    检测zip格式压缩保是否加密
    file: 文件对象
    return {True:文件加密 False：文件没加密}
    '''
    zf = zipfile.ZipFile(file)
    for zinfo in zf.infolist():
        is_encrypted = zinfo.flag_bits & 0x1
        if is_encrypted:
            return True
        else:
            return False



def des_encrypt_file(file_path, secret_key: str):
    """
    DES加密文件
    :param file_path:
    :param secret_key:
    :return:
    """
    with open(file_path, "rb+") as f:
        cipher2 = DES.new(secret_key.encode(), DES.MODE_ECB)
        data = pad(f.read(), 8)
        en = cipher2.encrypt(data)
        f.seek(0)
        f.truncate()
        f.write(en)


def des_descrypt_file(file_path, secret_key: str):
    """
    DES解密文件
    :param file_path:
    :param secret_key:
    :return:
    """
    with open(file_path, "rb+") as f:
        cipher2 = DES.new(secret_key.encode(), DES.MODE_ECB)
        de = cipher2.decrypt(f.read())
        f.seek(0)
        f.truncate()
        f.write(de)
