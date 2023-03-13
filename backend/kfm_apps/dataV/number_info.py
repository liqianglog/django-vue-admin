# -*- coding: utf-8 -*-
import calendar
from datetime import datetime

from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncDay
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from basics_manage.models import DeviceManage
from carton_manage.code_manage.models import CodePackage
from carton_manage.production_manage.models import ProductionWork
from carton_manage.verify_manage.models import CameraManage, VerifyWorkOrder, VerifyCodeRecord
from dvadmin.utils.json_response import DetailResponse
from utils.date_tools import dateRange


class NumberInfoApiView(APIView):
    '''数量信息接口'''
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        获取数量信息
        :param request:
        :return:
        {
            codepackage_total  码包订单总数
            codepackage_repetition_total 码包重码总数
            prod_work_total  生产订单总数
            camera_total 相机总数
            verify_work_order_total 检测工单总数
            verify_code_record_total 检测码问题总数
        }
        """
        _codepackage_total = CodePackage.objects.aggregate(total_number=Sum('total_number'))
        codepackage_total = _codepackage_total.get('total_number') or 0
        _codepackage_repetition_total = CodePackage.objects.aggregate(total_number=Sum('package_repetition_number'))
        codepackage_repetition_total = _codepackage_repetition_total.get('total_number') or 0
        _prod_work_total = ProductionWork.objects.count()
        _camera_total = CameraManage.objects.count()
        _verify_work_order_total = VerifyWorkOrder.objects.count()
        _verify_code_record_total = VerifyCodeRecord.objects.count()
        data = {
            "codepackage_total": codepackage_total,
            "codepackage_repetition_total": codepackage_repetition_total,
            "prod_work_total": _prod_work_total,
            "camera_total": _camera_total,
            "verify_work_order_total": _verify_work_order_total,
            "verify_code_record_total": _verify_code_record_total
        }
        return DetailResponse(data=data)


class CodePackageRepetitionPieAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        码包重码数对比(环形图)
        """
        _codepackage = CodePackage.objects.aggregate(
            Sum('database_repetition_number'),
            Sum('package_repetition_number')
        )
        data = {
            'package_repetition_number': _codepackage.get('package_repetition_number__sum'),
            'database_repetition_number': _codepackage.get('database_repetition_number__sum')
        }
        return DetailResponse(data=data)


class DeviceInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        设备信息
        """
        _device = DeviceManage.objects.values('id', 'no', 'name', 'type')
        _device_info = _device.aggregate(
            total=Count('id'),
            verify_device=Count('id', filter=Q(type=1)),
            prod_device=Count('id', filter=Q(type=0))
        )
        data = {
            "device_total": _device_info.get('total'),
            "verify_device": _device_info.get('verify_device'),
            "prod_device": _device_info.get('prod_device'),
            "list": _device[:5]
        }
        return DetailResponse(data=data)


class ProductionWorkAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        当月每日生产工单情况
         1. 新增生产工单数
         2. 码包下载数
         3. 生产前校验数
        """
        today = datetime.now()
        year = today.year
        month = today.month
        this_month_start = datetime(year, month, 1)
        this_month_end = datetime(year, month, calendar.monthrange(year, month)[1])
        _productionwork = ProductionWork.objects.filter(
            create_datetime__year=year,
            create_datetime__month=month
        ).annotate(
            day=TruncDay('create_datetime')
        ).values('day').annotate(
            prod_number=Count('id'),
            download_number=Count('codepackage_download_prod_work'),
            verify_number=Count('verify_record_prod_work')
        )
        date_list = dateRange(this_month_start, this_month_end)
        prod_number_list = [0 for _ in range(len(date_list))]
        download_number_list = [0 for _ in range(len(date_list))]
        verify_number_list = [0 for _ in range(len(date_list))]
        for item in _productionwork:
            index = item['day'].strftime("%Y-%m-%d")
            prod_number_list[date_list.index(index)] = item['prod_number']
            download_number_list[date_list.index(index)] = item['download_number']
            verify_number_list[date_list.index(index)] = item['verify_number']
        data = {
            "date_list": date_list,
            "prod_number_list": prod_number_list,
            "download_number_list": download_number_list,
            "verify_number_list": verify_number_list
        }
        return DetailResponse(data=data)


class VerifyCodeRecordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        每日检测问题码数
        """
        today = datetime.now()
        year = today.year
        month = today.month
        day = today.day
        _verifyrecord = VerifyCodeRecord.objects.filter(
            create_datetime__year=year,
            create_datetime__month=month,
            create_datetime__day=day
        ).aggregate(
            total=Count('id'),
            error_0=Count('id', filter=Q(error_type=0)),
            error_2=Count('id', filter=Q(error_type=2)),
            error_3=Count('id', filter=Q(error_type=3)),
            error_4=Count('id', filter=Q(error_type=4)),
            error_5=Count('id', filter=Q(error_type=5)),
        )
        data = {
            "verify_total": _verifyrecord.get('total'),
            "verify_error_type_0": _verifyrecord.get('error_0'),
            "verify_error_type_2": _verifyrecord.get('error_2'),
            "verify_error_type_3": _verifyrecord.get('error_3'),
            "verify_error_type_4": _verifyrecord.get('error_4'),
            "verify_error_type_5": _verifyrecord.get('error_5'),
        }
        return DetailResponse(data=data)


class VerifyCodePieAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        问题码占比情况
        """
        _verifyrecord = VerifyCodeRecord.objects.aggregate(
            total=Count('id'),
            error_0=Count('id', filter=Q(error_type=0)),
            error_2=Count('id', filter=Q(error_type=2)),
            error_3=Count('id', filter=Q(error_type=3)),
            error_4=Count('id', filter=Q(error_type=4)),
            error_5=Count('id', filter=Q(error_type=5)),
        )
        data = {
            "name_list": ["未识别码", "码不存在", "本检测包重码", "本生产工单重码", "非本生产工单码"],
            "data": [
                {
                    "name": "未识别码",
                    "value": _verifyrecord.get("error_type_0") or 0,
                },
                {
                    "name": "码不存在",
                    "value": _verifyrecord.get("error_type_2") or 0,
                },
                {
                    "name": "本检测包重码",
                    "value": _verifyrecord.get("error_type_3") or 0,
                },
                {
                    "name": "本生产工单重码",
                    "value": _verifyrecord.get("error_type_4") or 0,
                },
                {
                    "name": "非本生产工单码",
                    "value": _verifyrecord.get("error_type_5") or 0
                }
            ]
        }
        return DetailResponse(data=data)
