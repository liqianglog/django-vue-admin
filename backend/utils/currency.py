"""
通用方法封装
"""
import os
import subprocess
import zipfile
from hashlib import md5

from django.conf import settings

from application.settings import BASE_DIR, DEBUG, ORDER_IMPORT_PATH, PRODUCTION_ORDER_ZIP_PATH, \
    PRODUCTION_ORDER_FILE_PATH


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
        print(f"222-----{cmd}")
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


def zip_package_split(file_path, unpack_list):
    """
    zip 拆包
    :param file_path:
    :param unpack_list:
    :return:
    """
    order_file_path = get_order_import_path()
    flag = 0  # 计数
    digit = 1  # 文件数
    data = ""
    file_paths = []
    with zipfile.ZipFile(os.path.join(order_file_path, file_path)) as zip:
        with zip.open(zip.namelist()[0]) as file:
            for line in file:
                flag += 1
                data += line.decode()
                if flag == unpack_list[digit - 1]:
                    txt_file_path = file_path.replace('.zip', f'_{digit}.txt')

                    with open(os.path.join(order_file_path, txt_file_path), "w") as new_f:
                        new_f.write(data)
                    zip_file_url = txt_file_path.replace('.txt', '.zip')
                    # 进行zip 压缩
                    zip_compress_file(os.path.join(order_file_path, txt_file_path),
                                      os.path.join(order_file_path, zip_file_url))
                    # 删除txt 文件
                    os.remove(os.path.join(order_file_path, txt_file_path))
                    file_paths.append(zip_file_url)
                    flag = 0
                    digit += 1
                    data = ""
                    if len(unpack_list) < digit:
                        break

    return file_paths


def get_order_import_path():
    """
    订单管理导入文件路径
    :return:
    """
    from django.db import connection
    path = os.path.join(BASE_DIR, 'kfm_code_file', 'upload_file', connection.tenant.schema_name)
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


def get_production_order_zip_path():
    """
    生产工单文件汇总后 zip 目录
    :return:
    """
    from django.db import connection
    path = os.path.join(BASE_DIR, PRODUCTION_ORDER_ZIP_PATH, connection.tenant.schema_name)
    if not os.path.exists(path):  # 文件夹不存在则创建
        os.makedirs(path)
    return path


def get_production_order_file_path():
    """
    生产订单上传文件路径
    :return:
    """
    from django.db import connection
    path = os.path.join(BASE_DIR, PRODUCTION_ORDER_FILE_PATH, connection.tenant.schema_name)
    if not os.path.exists(path):  # 文件夹不存在则创建
        os.makedirs(path)
    return path
