# 导出excel数据
import hashlib
import os
import time

import xlrd
import xlwt
from django.conf import settings

from apps.vadmin.system.models import SaveFile
from apps.vadmin.system.serializers import SaveFileSerializer


def len_byte(value):
    # 获取字符串长度，一个中文的长度为2
    length = len(value)
    utf8_length = len(value.encode('utf-8'))
    length = (utf8_length - length) / 2 + length
    return int(length)


def export_excel(field_data: list, data: list, FileName: str, file_path: str = settings.MEDIA_ROOT):
    """
    Excel导出
    :param data: 数据源
    :param field_data: 首行数据源
    :param file_path: 文件保存路径
    :param FileName: 文件保存名字
    :return:
    """
    wbk = xlwt.Workbook(encoding='utf-8')
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)  # 第二参数用于确认同一个cell单元是否可以重设值。
    style = xlwt.XFStyle()  # 赋值style为XFStyle()，初始化样式
    # 设置居中
    wbk.set_colour_RGB(0x23, 0, 60, 139)
    xlwt.add_palette_colour("custom_colour_35", 0x23)
    tab_al = xlwt.Alignment()
    tab_al.horz = 0x02  # 设置水平居中
    tab_al.vert = 0x01  # 设置垂直居中
    # 设置表头单元格背景颜色
    tab_pattern = xlwt.Pattern()  # 创建一个模式
    tab_pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # 设置其模式为实型
    tab_pattern.pattern_fore_colour = 55
    # 设置单元格内字体样式
    tab_fnt = xlwt.Font()  # 创建一个文本格式，包括字体、字号和颜色样式特性
    tab_fnt.height = 200
    default_width = 14
    tab_fnt.name = u'楷体'  # 设置其字体为微软雅黑
    tab_fnt.colour_index = 1  # 设置其字体颜色
    # 设置单元格下框线样式
    tab_borders = xlwt.Borders()
    tab_borders.left = xlwt.Borders.THIN
    tab_borders.right = xlwt.Borders.THIN
    tab_borders.top = xlwt.Borders.THIN
    tab_borders.bottom = xlwt.Borders.THIN
    tab_borders.left_colour = 23
    tab_borders.right_colour = 23
    tab_borders.bottom_colour = 23
    tab_borders.top_colour = 23
    #### 把数据写入excel中
    # 所有表格单元格样式
    # 先生成表头
    style.alignment = tab_al  # 设置居中
    style.pattern = tab_pattern  # 设置表头单元格背景颜色
    style.font = tab_fnt  # 设置单元格内字体样式
    style.borders = tab_borders
    for index, ele in enumerate(field_data):
        sheet.write_merge(0, 0, index, index, ele, style)  # (列开始, 列结束, 行开始, 行结束, '数据内容')

    # 确定栏位宽度
    col_width = []
    for index, ele in enumerate(data):
        for inx, values in enumerate(ele.values()):
            if index == 0:
                col_width.append(len_byte(str(values)))
            else:
                if col_width[inx] < len_byte(str(values)):
                    col_width[inx] = len_byte(str(values))
    # 设置栏位宽度，栏位宽度小于10时候采用默认宽度
    for i in range(len(col_width)):
        if col_width[i] > 10:
            width = col_width[i] if col_width[i] < 36 else 36
            sheet.col(i).width = 256 * (width + 6)
        else:
            sheet.col(i).width = 256 * (default_width)

    row = 1
    # 内容背景颜色
    left_pattern = xlwt.Pattern()  # 创建一个模式
    left_pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # 设置其模式为实型
    left_pattern.pattern_fore_colour = 1

    # 设置单元格内字体样式
    left_fnt = xlwt.Font()  # 创建一个文本格式，包括字体、字号和颜色样式特性
    left_fnt.height = 200
    left_fnt.name = u'楷体'  # 设置其字体为微软雅黑
    left_fnt.colour_index = 0  # 设置其字体颜色

    left_style = style
    left_style.pattern = left_pattern
    left_style.font = left_fnt

    for results in data:
        for index, values in enumerate(results.values()):
            sheet.write(row, index, label=values, style=left_style)
        row += 1

    monthTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    pathRoot = os.path.join(file_path, 'system', monthTime)
    if not os.path.exists(pathRoot):
        os.makedirs(pathRoot)
    path_name = os.path.join(pathRoot, FileName)
    wbk.save(path_name)
    return os.path.join('system', monthTime, FileName)


def export_excel_save_model(request, field_data, data, FilName):
    """
    导出Excel并保存到 SaveFile 文件管理中
    :param request:
    :param field_data: 首行数据源
    :param data: 数据源
    :param FilName: 文件名
    :return:
    """
    # 根据生成的字典MD5
    time_stamp = hashlib.md5(str(field_data).encode('utf8')).hexdigest()
    # 存入文件数据库中
    FilName = '.'.join(FilName.split('.')[:-1]) + str(time_stamp) + '.' + FilName.split('.')[-1]
    file_rul = export_excel(field_data=field_data, data=data, FileName=FilName)
    savefile, _ = SaveFile.objects.get_or_create(file=file_rul)
    if _ == True:
        savefile.name = FilName
        savefile.type = 'application/vnd.ms-excel'
        savefile.size = os.path.getsize(os.path.join(settings.MEDIA_ROOT, file_rul))
        savefile.address = '本地存储'
        savefile.source = '导出'
        savefile.creator = request.user
        savefile.dept_belong_id = getattr(request.user, 'dept_id', None)
    savefile.modifier = request.user.username
    savefile.save()
    return SaveFileSerializer(savefile).data


def excel_to_data(file_url, field_data):
    """
    读取导入的excel文件
    :param request:
    :param field_data: 首行数据源
    :param data: 数据源
    :param FilName: 文件名
    :return:
    """
    # 读取excel 文件
    data = xlrd.open_workbook(os.path.join(settings.BASE_DIR.replace('\\', os.sep), *file_url.split(os.sep)))
    table = data.sheets()[0]
    # 创建一个空列表，存储Excel的数据
    tables = []
    for i, rown in enumerate(range(table.nrows)):
        if i == 0: continue
        array = {}
        for index, ele in enumerate(field_data.keys()):
            cell_value = table.cell_value(rown, index)
            # 由于excel导入数字类型后，会出现数字加 .0 的，进行处理
            if type(cell_value) is float and str(cell_value).split('.')[1] == '0':
                cell_value = int(str(cell_value).split('.')[0])
            if type(cell_value) is str:
                cell_value = cell_value.strip(' \t\n\r')
            array[ele] = cell_value

        tables.append(array)
    return tables
