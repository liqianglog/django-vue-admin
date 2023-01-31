from django.test import TestCase

# Create your tests here.
from utils.currency import read_max_row, md5_file
file_path = '/Users/liqiang/Downloads/200w_测试包材供应商_20230131235755156364.txt'
total_number = read_max_row(file_path).get('count')  # 文件总行数
file_md5 = md5_file(file_path)  # 文件MD5 值
print(total_number,file_md5)
