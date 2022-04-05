# -*- coding: utf-8 -*-
import os

import openpyxl
from django.conf import settings


def import_to_data(file_url, field_data):
    """
    读取导入的excel文件
    :param request:
    :param field_data: 首行数据源
    :param data: 数据源
    :param FilName: 文件名
    :return:
    """
    # 读取excel 文件
    file_path = os.path.join(settings.MEDIA_ROOT, file_url)
    file_path_dir = os.path.join(settings.BASE_DIR, file_path)
    workbook = openpyxl.load_workbook(file_path_dir)
    table = workbook[workbook.sheetnames[0]]
    # 创建一个空列表，存储Excel的数据
    tables = []
    for i, row in enumerate(range(table.max_row)):
        if i == 0: continue
        array = {}
        for index, ele in enumerate(field_data.keys()):
            cell_value = table.cell(row=row + 1, column=index + 2).value
            # 由于excel导入数字类型后，会出现数字加 .0 的，进行处理
            if type(cell_value) is float and str(cell_value).split('.')[1] == '0':
                cell_value = int(str(cell_value).split('.')[0])
            if type(cell_value) is str:
                cell_value = cell_value.strip(' \t\n\r')
            array[ele] = cell_value
        tables.append(array)
    return tables
