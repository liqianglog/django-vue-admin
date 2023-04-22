#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/14 15:49
# @Author  : harry
import datetime
import json
import re
import time

from django.db.models import Count, Sum, Q
from django.db.models.functions import TruncMonth, TruncDay
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from conf.env import DATABASE_USER, DATABASE_NAME
from dvadmin.system.models import Users, LoginLog, FileList
from dvadmin.system.views.login_log import LoginLogSerializer
from dvadmin.utils.json_response import DetailResponse
from django.db import connection
from django.utils.timezone import now
from django.db.models import Count
from django.db.models.functions import TruncDate

from dvadmin.utils.string_util import format_bytes


def jx_timestamp():
    cur_time = datetime.datetime.now()
    a = datetime.datetime.strftime(cur_time, '%Y-%m-%d %H:%M:%S')
    timeStamp = int(time.mktime(time.strptime(a, "%Y-%m-%d %H:%M:%S")))
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


class DataVViewSet(GenericViewSet):
    queryset = LoginLog.objects.all()
    serializer_class = LoginLogSerializer
    extra_filter_backends = []
    ordering_fields = ['create_datetime']

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def users_login_total(self, request):
        """
        用户登录总数数据
        :param request:
        :return:
        """
        login_total = LoginLog.objects.all().count()
        return DetailResponse(data={"login_total": login_total}, msg="获取成功")

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def users_total(self, request):
        """
        用户总数
        :param request:
        :return:
        """
        users_total = Users.objects.all().count()
        return DetailResponse(data={"users_total": users_total, }, msg="获取成功")

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def attachment_total(self, request):
        """
        附件统计数据
        :param request:
        :return:
        """
        count = FileList.objects.all().count()
        data = FileList.objects.aggregate(sum_size=Sum('size'))
        return DetailResponse(data={"count": count, "occupy_space": format_bytes(data.get('sum_size') or 0)}, msg="获取成功")

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def database_total(self, request):
        """
        数据库统计数据
        :param request:
        :return:
        """
        count = len(connection.introspection.table_names())
        database_type = connection.settings_dict['ENGINE']
        sql = None
        if 'mysql' in database_type:
            sql = "SELECT SUM(data_length + index_length) AS size FROM information_schema.TABLES WHERE table_schema = DATABASE()"
        elif 'postgres' in database_type or 'psqlextra' in database_type:
            sql = """SELECT SUM(pg_total_relation_size(quote_ident(schemaname) || '.' || quote_ident(tablename))) AS size FROM pg_tables WHERE schemaname = current_schema();"""
        elif 'oracle' in database_type:
            sql = "SELECT SUM(bytes) AS size FROM user_segments"
        elif 'microsoft' in database_type:
            sql = "SELECT SUM(size) * 8 AS size FROM sys.database_files"
        else:
            space = 0
        if sql:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    space = result[0]
                except Exception as e:
                    print(e)
                    space = '无权限'
        return DetailResponse(data={"count": count, "space": format_bytes(space or 0)}, msg="获取成功")

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def registered_user(self, request):
        """
        用户注册趋势
        :param request:
        :return:
        """
        today = datetime.datetime.today()
        seven_days_ago = today - datetime.timedelta(days=30)

        users = Users.objects.filter(date_joined__gte=seven_days_ago).annotate(day=TruncDay('date_joined')).values(
            'day').annotate(count=Count('id'))

        result = []
        for i in range(30):
            date = (today - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            count = 0
            for user in users:
                if user['day'] == date:
                    count = user['count']
                    break
            result.append({'day': date, 'count': count})

        # users_last_month = Users.objects.filter(date_joined__gte=last_month).annotate(day=TruncDate('date_joined')).values('day').annotate(count=Count('id'))
        return DetailResponse(data={"registered_user_list": result}, msg="获取成功")

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def registered_user(self, request):
        """
        用户注册趋势
        :param request:
        :return:
        """
        day = 30
        today = datetime.datetime.today()
        seven_days_ago = today - datetime.timedelta(days=day)
        users = Users.objects.filter(create_datetime__gte=seven_days_ago).annotate(
            day=TruncDay('create_datetime')).values(
            'day').annotate(count=Count('id')).order_by('-day')
        result = []
        data_dict = {ele.get('day').strftime('%Y-%m-%d'): ele.get('count') for ele in users}
        for i in range(day):
            date = (today - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            result.append({'day': date, 'count': data_dict[date] if date in data_dict else 0})
        result = sorted(result, key=lambda x: x['day'])
        return DetailResponse(data={"registered_user_list": result}, msg="获取成功")

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def login_user(self, request):
        """
        用户登录趋势
        :param request:
        :return:
        """
        day = 30
        today = datetime.datetime.today()
        seven_days_ago = today - datetime.timedelta(days=day)
        users = LoginLog.objects.filter(create_datetime__gte=seven_days_ago).annotate(
            day=TruncDay('create_datetime')).values(
            'day').annotate(count=Count('id')).order_by('-day')
        result = []
        data_dict = {ele.get('day').strftime('%Y-%m-%d'): ele.get('count') for ele in users}
        for i in range(day):
            date = (today - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            result.append({'day': date, 'count': data_dict[date] if date in data_dict else 0})
        result = sorted(result, key=lambda x: x['day'])
        return DetailResponse(data={"login_user": result}, msg="获取成功")

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def users_active(self, request):
        """
        用户新增活跃数据统计
        :param request:
        :return:
        """
        today = datetime.date.today()
        seven_days_ago = today - datetime.timedelta(days=6)
        thirty_days_ago = today - datetime.timedelta(days=29)

        today_users = Users.objects.filter(date_joined__date=today).count()
        today_logins = Users.objects.filter(last_login__date=today).count()
        three_days_users = Users.objects.filter(date_joined__gte=seven_days_ago).count()
        seven_days_users = Users.objects.filter(date_joined__gte=thirty_days_ago).count()
        seven_days_active = Users.objects.filter(last_login__gte=seven_days_ago).values('last_login').annotate(
            count=Count('id', distinct=True)).count()
        monthly_active = Users.objects.filter(last_login__gte=thirty_days_ago).values('last_login').annotate(
            count=Count('id', distinct=True)).count()

        data = {
            'today_users': today_users,
            'today_logins': today_logins,
            'three_days': three_days_users,
            'seven_days': seven_days_users,
            'seven_days_active': seven_days_active,
            'monthly_active': monthly_active
        }
        return DetailResponse(data=data, msg="获取成功")

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def login_region(self, request):
        """
        登录用户区域分布
        :param request:
        :return:
        """
        CHINA_PROVINCES = [
            {'name': '北京', 'code': '110000'},
            {'name': '天津', 'code': '120000'},
            {'name': '河北', 'code': '130000'},
            {'name': '山西', 'code': '140000'},
            {'name': '内蒙古', 'code': '150000'},
            {'name': '辽宁', 'code': '210000'},
            {'name': '吉林', 'code': '220000'},
            {'name': '黑龙江', 'code': '230000'},
            {'name': '上海', 'code': '310000'},
            {'name': '江苏', 'code': '320000'},
            {'name': '浙江', 'code': '330000'},
            {'name': '安徽', 'code': '340000'},
            {'name': '福建', 'code': '350000'},
            {'name': '江西', 'code': '360000'},
            {'name': '山东', 'code': '370000'},
            {'name': '河南', 'code': '410000'},
            {'name': '湖北', 'code': '420000'},
            {'name': '湖南', 'code': '430000'},
            {'name': '广东', 'code': '440000'},
            {'name': '广西', 'code': '450000'},
            {'name': '海南', 'code': '460000'},
            {'name': '重庆', 'code': '500000'},
            {'name': '四川', 'code': '510000'},
            {'name': '贵州', 'code': '520000'},
            {'name': '云南', 'code': '530000'},
            {'name': '西藏', 'code': '540000'},
            {'name': '陕西', 'code': '610000'},
            {'name': '甘肃', 'code': '620000'},
            {'name': '青海', 'code': '630000'},
            {'name': '宁夏', 'code': '640000'},
            {'name': '新疆', 'code': '650000'},
            {'name': '台湾', 'code': '710000'},
            {'name': '香港', 'code': '810000'},
            {'name': '澳门', 'code': '820000'},
            {'name': '未知区域', 'code': '000000'},
        ]
        provinces = [x['name'] for x in CHINA_PROVINCES]
        day = 30
        today = datetime.datetime.today()
        seven_days_ago = today - datetime.timedelta(days=day)
        province_data = LoginLog.objects.filter(create_datetime__gte=seven_days_ago).values('province').annotate(
            count=Count('id')).order_by('-count')
        province_dict = {p: 0 for p in provinces}
        for ele in province_data:
            if ele.get('province') in province_dict:
                province_dict[ele.get('province')] += ele.get('count')
            else:
                province_dict['未知区域'] += ele.get('count')
        data = [{'region': key, 'count': val} for key, val in province_dict.items()]
        data = sorted(data, key=lambda x: x['count'], reverse=True)
        return DetailResponse(data=data, msg="获取成功")
