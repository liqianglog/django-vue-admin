import datetime
import logging
import sys
import time

import psutil

from apps.vadmin.monitor.models import Server, Monitor, SysFiles
from apps.vadmin.op_drf.response import SuccessResponse
from apps.vadmin.system.models import ConfigSettings
from apps.vadmin.utils.decorators import BaseCeleryApp

logger = logging.getLogger(__name__)
from platform import platform


def getIP():
    """获取ipv4地址"""
    dic = psutil.net_if_addrs()
    ipv4_list = []
    for adapter in dic:
        snicList = dic[adapter]
        for snic in snicList:
            if snic.family.name == 'AF_INET':
                ipv4 = snic.address
                if ipv4 != '127.0.0.1':
                    ipv4_list.append(ipv4)
    if len(ipv4_list) >= 1:
        return ipv4_list[0]
    else:
        return None


@BaseCeleryApp(name='apps.vadmin.monitor.tasks.get_monitor_info', save_success_logs=False)
def get_monitor_info():
    """
    定时获取系统监控信息
    :return:
    """
    # 获取服务器
    ip = getIP()
    if not ip:
        logger.error("无法获取到IP")
        return
    server_obj, create = Server.objects.get_or_create(ip=ip)
    if create:
        server_obj.name = ip
        terse = ('terse' in sys.argv or '--terse' in sys.argv)
        aliased = (not 'nonaliased' in sys.argv and not '--nonaliased' in sys.argv)
        server_obj.os = platform(aliased, terse)
        server_obj.save()

    # 获取CPU和内存信息
    mem = psutil.virtual_memory()
    monitor_obj = Monitor()
    monitor_obj.cpu_num = psutil.cpu_count()
    monitor_obj.cpu_sys = float(psutil.cpu_percent(0.1))
    monitor_obj.mem_num = int(mem.total / 1024)
    monitor_obj.mem_sys = int(mem.used / 1024)
    monitor_obj.seconds = time.strftime("%d天 %H 小时 %M 分 %S 秒", time.gmtime(int(time.time()) - int(psutil.boot_time())))
    monitor_obj.server = server_obj
    monitor_obj.save()

    # 保存磁盘信息
    for ele in psutil.disk_partitions():
        disk = psutil.disk_usage('/')

        sys_files_obj = SysFiles()
        sys_files_obj.dir_name = ele.mountpoint
        sys_files_obj.sys_type_name = ele.opts
        sys_files_obj.type_name = ele.fstype
        sys_files_obj.total = disk.total
        sys_files_obj.disk_sys = disk.used
        sys_files_obj.monitor = monitor_obj
        sys_files_obj.save()

    return SuccessResponse(msg="")


@BaseCeleryApp(name='apps.vadmin.monitor.tasks.clean_surplus_monitor_info')
def clean_surplus_monitor_info():
    """
    定时清理多余 系统监控信息
    :return:
    """
    config_settings_obj = ConfigSettings.objects.filter(configKey='sys.monitor.info.save_days').first()
    today = datetime.datetime.now().date()
    clean_day_before = today - datetime.timedelta(days=int(config_settings_obj.configValue or 30))
    Monitor.objects.filter(update_datetime__lt=clean_day_before).delete()
    logger.info(f"成功清空{config_settings_obj.configValue}天前数据")
