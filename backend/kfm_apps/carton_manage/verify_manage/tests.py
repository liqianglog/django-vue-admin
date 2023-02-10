import os
from datetime import datetime
from application import settings
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()
from django.test import TestCase

# Create your tests here.
# 生产检测回传测试码文件包
from dvadmin.utils.string_util import random_str
from utils.currency import des_encrypt_file, zip_compress_file, md5_file


def make_zip(secret_key, code_number=1000, unrecognized_numer=0, repeat=0, same_repeat=1, invalid_number=0,
             this_production_order_code=[], not_this_production_order_code=[]):
    """
    code_number: 需要生成正常码的数量
    unrecognized_numer: 生成未识别码数量
    repeat: 生成本检测包重码数量
    same_repeat: 同一个码重码次数
    invalid_number: 生成码不存在个数
    this_production_order_code: 生成本生产工单重码
    not_this_production_order_code: 生成非本生产工单码
    """
    file_path = os.path.join(os.getcwd(), 'demo.txt')
    with open(os.path.join(os.getcwd(), 'demo.txt'), 'w') as f:
        with open(os.path.join(os.getcwd(), 'code_test.txt')) as f1:
            for index, readline in enumerate(f1.readlines()):
                if index >= code_number:
                    break
                code = readline.replace('\n', '').split(',')[1]
                f.write(f'{code},{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        # 添加未识别模拟数据
        if unrecognized_numer:
            for ele in range(unrecognized_numer):
                f.write(f'000000,{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            # 添加本码包重码数
        if repeat:
            with open(os.path.join(os.getcwd(), 'code_test.txt')) as f1:
                for index, readline in enumerate(f1.readlines()):
                    if index >= repeat:
                        break
                    code = readline.replace('\n', '').split(',')[1]
                    for ele in range(same_repeat):
                        f.write(f'{code},{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            # 生成无效码
            if invalid_number:
                for ele in range(invalid_number):
                    f.write(f'HTTPS://KD4.CN/W004/{random_str()},{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            # 生成本生产工单重码
            if this_production_order_code:
                for ele in this_production_order_code:
                    f.write(f'{ele},{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            # 生成非本生产工单码
            if not_this_production_order_code:
                for ele in not_this_production_order_code:
                    f.write(f'{ele},{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
    # zip压缩
    zip_file_path = file_path.replace('.txt', '.zip')
    zip_compress_file(file_path, zip_file_path)
    # 进行加密
    des_encrypt_file(zip_file_path, secret_key)
    # 打印MD5值
    print(md5_file(zip_file_path))


if __name__ == '__main__':
    # 根据发码的txt
    # 1. 生成正常的检测
    code_number = 1000  # 需要生成正常码的数量
    # 2. 生成存在未识别
    unrecognized_numer = 0
    # 3. 生成本检测包重码
    repeat = 3
    same_repeat = 3  # 同一个码重码次数
    # 4. 生成码不存在
    invalid_number = 10
    # 5. 生成本生产工单重码
    this_production_order_code = []
    # 6. 生成非本生产工单码
    not_this_production_order_code = []

    secret_key = settings.ENCRYPTION_KEY_ID[1]
    make_zip(
        secret_key,
        code_number=code_number,
        unrecognized_numer=unrecognized_numer,
        repeat=repeat,
        same_repeat=same_repeat,
        invalid_number=invalid_number,
        this_production_order_code=this_production_order_code,
        not_this_production_order_code=not_this_production_order_code
    )
    print(
        f"总计生成码数量: {code_number + unrecognized_numer + repeat * same_repeat + invalid_number + len(this_production_order_code) + len(not_this_production_order_code)}")
