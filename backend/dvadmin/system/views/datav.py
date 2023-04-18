#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/14 15:49
# @Author  : harry
import datetime
import json
import re
import time

from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from conf.env import DATABASE_USER, DATABASE_NAME
from dvadmin.system.models import Users, LoginLog, FileList
from dvadmin.system.views.login_log import LoginLogSerializer
from dvadmin.utils.json_response import DetailResponse
from django.db import connection


def jx_timestamp():
    cur_time = datetime.datetime.now()
    a = datetime.datetime.strftime(cur_time, '%Y-%m-%d %H:%M:%S')
    timeStamp = int(time.mktime(time.strptime(a, "%Y-%m-%d %H:%M:%S")))
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


class DataVViewSet(GenericViewSet):
    permission_classes = []
    queryset = LoginLog.objects.all()
    serializer_class = LoginLogSerializer
    extra_filter_backends = []
    ordering_fields = ['create_datetime']

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def homepage_statistics(self, request):
        # Users  新增
        # LoginLog  # 最后登录
        timestr = jx_timestamp().split(" ")
        min_time = datetime.datetime.strptime(timestr[0] + " " + "00:00:00", "%Y-%m-%d %H:%M:%S")
        max_time = datetime.datetime.strptime(timestr[0] + " " + "23:59:59", "%Y-%m-%d %H:%M:%S")
        # 今日注册
        today_register = Users.objects.filter(create_datetime__gte=min_time, is_superuser=0).count()
        # 今日登录
        today_login = len(set(LoginLog.objects.filter(create_datetime__gte=min_time).values_list('username')))
        # 三日新增
        Three_days_register = Users.objects.filter(
            create_datetime__gte=min_time - datetime.timedelta(days=3), is_superuser=0).count()
        # 七日新增
        Seven_days_register = Users.objects.filter(
            create_datetime__gte=min_time - datetime.timedelta(days=7), is_superuser=0).count()
        # 七日活跃
        Seven_days_login = len(set(LoginLog.objects.filter(
            create_datetime__gte=min_time - datetime.timedelta(days=7)).values_list('username')))
        # 月活跃
        month_login = len(set(LoginLog.objects.filter(
            create_datetime__gte=min_time - datetime.timedelta(days=30)).values_list('username')))
        # 七日用户登录数
        sum_days_login_list = []
        for i in range(7):
            sum_days_login_list.append({"time": (min_time + datetime.timedelta(days=-i)).strftime("%Y-%m-%d"),
                                        "count": len(set(LoginLog.objects.filter(
                                            create_datetime__lte=max_time - datetime.timedelta(days=i),
                                            create_datetime__gte=min_time - datetime.timedelta(days=i)).values_list(
                                            'username')))})

        # 七日注册用户数
        sum_days_register_list = []
        for i in range(7):
            sum_days_register_list.append(
                {"time": (min_time + datetime.timedelta(days=-i)).strftime("%Y-%m-%d"), "count": Users.objects.filter(
                    create_datetime__lte=max_time - datetime.timedelta(days=i),
                    create_datetime__gte=min_time - datetime.timedelta(days=i), is_superuser=0).count()})
        # 用户总数
        sum_register = Users.objects.filter(is_superuser=0).count()
        # FileList  附件
        today_f_l = FileList.objects.filter(create_datetime__gte=min_time).count()
        sum_f_l = FileList.objects.all().count()
        # 今日附件
        today_file = {'count': today_f_l, "occupy_space": 0}
        # 总附件
        sum_file = {'count': sum_f_l, "occupy_space": 0}

        # 获取游标对象

        cursor = connection.cursor()

        # 拿到游标对象后执行sql语句

        cursor.execute("show tables;")

        # 获取所有的数据

        rows = cursor.fetchall()
        tables_list = []
        for row in rows:
            tables_list.append(row)
        # cursor.execute(
        #     "select table_schema as db, table_name as tb, table_rows as data_rows, index_length / 1024 as 'storage(KB)' from information_schema.tables where table_schema='{}';".format(
        #         DATABASE_NAME))
        cursor.execute(
            "select table_schema as table_db, sum(index_length) as storage,count(table_name ) as tables  from information_schema.tables group by table_schema having table_db='{}';".format(
                DATABASE_NAME))
        rows = cursor.fetchall()
        count = 0
        space = 0
        for row in rows:
            count = row[2]
            space = round(row[1] / 1024 / 1024, 2)
        database_info = {"count": count, "space": space}
        data = {
            "today_register": today_register,
            "today_login": today_login,
            "Three_days_register": Three_days_register,
            "Seven_days_register": Seven_days_register,
            "Seven_days_login": Seven_days_login,
            "month_login": month_login,
            "sum_days_login_list": sum_days_login_list,
            "sum_days_register_list": sum_days_register_list,
            "sum_register": sum_register,
            "today_file": today_file,
            "sum_file": sum_file,
            "database_info": database_info,
        }
        return DetailResponse(data=data, msg="获取成功")
