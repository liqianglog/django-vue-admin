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


def make_zip(secret_key):
    file_path = os.path.join(os.getcwd(), 'demo.txt')
    print(file_path)
    with open(os.path.join(os.getcwd(), 'demo.txt'), 'w') as f:
        for ele in range(1000):
            f.write(f'HTTPS://KD4.CN/W004/{random_str()},{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
    # zip压缩
    zip_file_path = file_path.replace('.txt', '.zip')
    zip_compress_file(file_path, zip_file_path)
    # 进行加密
    des_encrypt_file(zip_file_path, secret_key)
    # 打印MD5值
    print(md5_file(zip_file_path))


if __name__ == '__main__':

    secret_key = settings.ENCRYPTION_KEY_ID[1]
    make_zip(secret_key)
