# -*- coding: utf-8 -*-
from urllib.parse import quote

from django.db import transaction
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from rest_framework.request import Request

from dvadmin.utils.import_export import import_to_data
from dvadmin.utils.json_response import DetailResponse
from dvadmin.utils.request_util import get_verbose_name


class ImportSerializerMixin:
    """
    自定义导出模板、导入功能
    """
    # 导入字段
    import_field_dict = {}
    # 导入序列化器
    import_serializer_class = None

    @transaction.atomic  # Django 事务,防止出错
    def import_data(self, request: Request, *args, **kwargs):
        """
        导入模板
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        assert self.import_field_dict, (
                "'%s' 请配置对应的导出模板字段。"
                % self.__class__.__name__
        )
        # 导出模板
        if request.method == 'GET':
            # 示例数据
            queryset = self.filter_queryset(self.get_queryset())
            # 导出excel 表
            response = HttpResponse(content_type='application/msexcel')
            response['Access-Control-Expose-Headers'] = f'Content-Disposition'
            response['Content-Disposition'] = f'attachment;filename={quote(str(f"导入{get_verbose_name(queryset)}模板.xlsx"))}'
            wb = Workbook()
            ws = wb.active
            row = get_column_letter(len(self.import_field_dict) + 1)
            column = 10
            ws.append(['序号', *self.import_field_dict.values()])
            tab = Table(displayName="Table1", ref=f"A1:{row}{column}")  # 名称管理器
            style = TableStyleInfo(name='TableStyleLight11', showFirstColumn=True,
                                   showLastColumn=True, showRowStripes=True, showColumnStripes=True)
            tab.tableStyleInfo = style
            ws.add_table(tab)
            wb.save(response)
            return response

        updateSupport = request.data.get('updateSupport')
        # 从excel中组织对应的数据结构，然后使用序列化器保存
        data = import_to_data(request.data.get('url'), self.import_field_dict)
        queryset = self.filter_queryset(self.get_queryset())
        unique_list = [ele.attname for ele in queryset.model._meta.get_fields() if
                       hasattr(ele, 'unique') and ele.unique == True]
        for ele in data:
            # 获取 unique 字段
            filter_dic = {i: ele.get(i) for i in list(set(self.import_field_dict.keys()) & set(unique_list))}
            print(11, ele)
            instance = filter_dic and queryset.filter(**filter_dic).first()
            print(22, instance)
            if instance and not updateSupport:
                continue
            if not filter_dic:
                instance = None
            serializer = self.import_serializer_class(instance, data=ele)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return DetailResponse(msg=f"导入成功！")


class ExportSerializerMixin:
    """
    自定义导出功能
    """
    # 导出字段
    export_field_label = []
    # 导出序列化器
    export_serializer_class = None

    def export_data(self, request: Request, *args, **kwargs):
        """
        导出功能
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        assert self.export_field_label, (
                "'%s' 请配置对应的导出模板字段。"
                % self.__class__.__name__
        )
        queryset = self.filter_queryset(self.get_queryset())
        data = self.export_serializer_class(queryset, many=True).data
        # 导出excel 表
        response = HttpResponse(content_type='application/msexcel')
        response['Access-Control-Expose-Headers'] = f'Content-Disposition'
        response['Content-Disposition'] = f'attachment;filename={quote(str(f"导出{get_verbose_name(queryset)}.xlsx"))}'
        wb = Workbook()
        ws = wb.active
        row = get_column_letter(len(self.export_field_label) + 1)
        column = 1
        ws.append(['序号', *self.export_field_label])
        for index, results in enumerate(data):
            ws.append([index + 1, *list(results.values())])
            column += 1
        tab = Table(displayName="Table2", ref=f"A1:{row}{column}")  # 名称管理器
        style = TableStyleInfo(name='TableStyleLight11', showFirstColumn=True,
                               showLastColumn=True, showRowStripes=True, showColumnStripes=True)
        tab.tableStyleInfo = style
        ws.add_table(tab)
        wb.save(response)
        return response
