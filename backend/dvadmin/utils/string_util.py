# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/8/21 021 9:48
@Remark:
"""
import hashlib
import random
from decimal import Decimal

CHAR_SET = ("2", "3", "4", "5",
            "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H",
            "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V",
            "W", "X", "Y", "Z")


def random_str(number=16):
    """
    返回特定长度的随机字符串(非进制)
    :return:
    """
    result = ""
    for i in range(0, number):
        inx = random.randint(0, len(CHAR_SET) - 1)
        result += CHAR_SET[inx]
    return result


def has_md5(str, salt='123456'):
    """
    md5 加密
    :param str:
    :param salt:
    :return:
    """
    # satl是盐值，默认是123456
    str = str + salt
    md = hashlib.md5()  # 构造一个md5对象
    md.update(str.encode())
    res = md.hexdigest()
    return res


def format_bytes(size, decimals=2):
    """
    格式化字节大小
    :param size:
    :param decimals:
    :return:
    """
    if isinstance(size, (str)) and size.isnumeric():
        size = int(size)
    elif not isinstance(size, (int, float, Decimal)):
        return size
    if size == 0:
        return "0 Bytes"
    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    i = 0
    while size >= 1024:
        size /= 1024
        i += 1

    return f"{round(size, decimals)} {units[i]}"
