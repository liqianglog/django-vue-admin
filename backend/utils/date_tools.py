# -*- coding: utf-8 -*-
import datetime


def dateRange(beginDate, endDate):
    """获取日期范围每日日期列表"""
    beginDate = str(beginDate.strftime("%Y-%m-%d"))
    endDate = str(endDate.strftime("%Y-%m-%d"))
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates
