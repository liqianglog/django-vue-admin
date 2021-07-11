from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
from rest_framework.request import Request

from apps.vadmin.monitor.filters import ServerFilter, MonitorFilter
from apps.vadmin.monitor.models import Server, Monitor, SysFiles
from apps.vadmin.monitor.serializers import ServerSerializer, MonitorSerializer, UpdateServerSerializer
from apps.vadmin.op_drf.response import SuccessResponse, ErrorResponse
from apps.vadmin.op_drf.viewsets import CustomModelViewSet
from apps.vadmin.permission.permissions import CommonPermission
from apps.vadmin.system.models import ConfigSettings


class ServerModelViewSet(CustomModelViewSet):
    """
    服务器信息 模型的CRUD视图
    """
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    update_serializer_class = UpdateServerSerializer
    # extra_filter_backends = [DataLevelPermissionsFilter]
    filter_class = ServerFilter
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    ordering = '-create_datetime'  # 默认排序


class MonitorModelViewSet(CustomModelViewSet):
    """
    服务器监控信息 模型的CRUD视图
    """
    queryset = Monitor.objects.all()
    serializer_class = MonitorSerializer
    # extra_filter_backends = [DataLevelPermissionsFilter]
    filter_class = MonitorFilter
    update_extra_permission_classes = (CommonPermission,)
    destroy_extra_permission_classes = (CommonPermission,)
    create_extra_permission_classes = (CommonPermission,)
    ordering = '-create_datetime'  # 默认排序

    def get_rate_info(self, request: Request, *args, **kwargs):
        """
        获取使用率 监控信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        pk = kwargs.get("pk")
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(server__id=pk).order_by("create_datetime")
        # 间隔取值
        queryset_count = queryset.count()
        Interval_num = 1 if queryset_count < 200 else int(queryset_count / 100)
        queryset = queryset.values('cpu_sys', 'mem_num', 'mem_sys', 'create_datetime')[::Interval_num][:100]
        data = {
            "cpu": [],
            "memory": [],
            "datetime": [],
        }
        for ele in queryset:
            data["cpu"].append(round(float(ele.get('cpu_sys', 0)), 2))
            data["datetime"].append(ele.get('create_datetime').strftime('%Y-%m-%d %H:%M:%S'))
            data["memory"].append(round(float(ele.get('mem_num', 0)), 4) and round(float(ele.get('mem_sys', 0)) /
                                                                                   float(ele.get('mem_num', 0)) * 100,
                                                                                   2))
        return SuccessResponse(data=data)

    def get_monitor_info(self, request: Request, *args, **kwargs):
        """
        最新的服务器状态信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        pk = kwargs.get("pk")
        instance = Monitor.objects.filter(server__id=pk).order_by("-create_datetime").first()
        if not instance:
            return ErrorResponse(msg="未找到服务器信息id")
        serializer = self.get_serializer(instance)
        data = serializer.data
        return SuccessResponse(data={
            "cpu": {
                "total": int(data.get('cpu_num'), 0),
                "used": "",  # cpu核心 可不传，如指cpu当前主频，该值可以传
                "rate": float(data.get('cpu_sys', 0)) / 100,
                "unit": "核心",  # 默认单位 核心
            },
            "memory": {
                "total": int(int(data.get('mem_num', 0)) / 1024),
                "used": int(int(data.get('mem_sys', 0)) / 1024),
                "rate": int(data.get('mem_num', 0)) and round(int(data.get('mem_sys', 0)) /
                                                              int(data.get('mem_num', 0)), 4),
                "unit": "MB",  # 默认单位 MB
            },
            "disk": [{
                "dir_name": ele.get('dir_name'),
                "total": int(int(ele.get('total', 0)) / 1024 / 1024 / 1024),
                "used": int(int(ele.get('disk_sys', 0)) / 1024 / 1024 / 1024),
                "rate": int(ele.get('total', 0)) and round(int(ele.get('disk_sys', 0)) / int(ele.get('total', 0)),
                                                           4),
                "unit": "GB",  # 默认单位 GB
            } for ele in SysFiles.objects.filter(monitor=instance).values('dir_name', 'total', 'disk_sys')]
        })

    def enabled_monitor_info(self, request: Request, *args, **kwargs):
        """
        更新和获取监控信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        enabled = request.query_params.get('enabled', None)
        save_days = request.query_params.get('save_days', None)
        interval = request.query_params.get('interval', None)
        # 定时获取系统监控信息
        periodictask_obj = PeriodicTask.objects.filter(task='apps.vadmin.monitor.tasks.get_monitor_info').first()
        if not periodictask_obj:
            intervalschedule_obj, _ = IntervalSchedule.objects.get_or_create(every=5, period="seconds")
            periodictask_obj = PeriodicTask()
            periodictask_obj.task = "apps.vadmin.monitor.tasks.get_monitor_info"
            periodictask_obj.name = "定时获取系统监控信息"
            periodictask_obj.interval = intervalschedule_obj
            periodictask_obj.enabled = False
            periodictask_obj.save()

        # 定时清理多余 系统监控信息
        clean_task_obj = PeriodicTask.objects.filter(
            task='apps.vadmin.monitor.tasks.clean_surplus_monitor_info').first()
        if not clean_task_obj:
            crontab_obj, _ = CrontabSchedule.objects.get_or_create(day_of_month="*", day_of_week="*", hour="1",
                                                                   minute="0", month_of_year="*")
            clean_task_obj = PeriodicTask()
            clean_task_obj.task = "apps.vadmin.monitor.tasks.clean_surplus_monitor_info"
            clean_task_obj.name = "定时清理多余-系统监控信息"
            clean_task_obj.crontab = crontab_obj
            clean_task_obj.enabled = True
            clean_task_obj.save()
        # 配置添加
        config_obj = ConfigSettings.objects.filter(configKey='sys.monitor.info.save_days').first()
        if not config_obj:
            config_obj = ConfigSettings()
            config_obj.configKey = "sys.monitor.info.save_days"
            config_obj.configName = "定时清理多余系统监控信息"
            config_obj.configValue = "30"
            config_obj.configType = "Y"
            config_obj.status = "1"
            config_obj.remark = "定时清理多余-系统监控信息，默认30天"
            config_obj.save()

        if enabled:
            # 更新监控状态
            periodictask_obj.enabled = True if enabled == "1" else False
            periodictask_obj.save()

            # 更新 定时清理多余 系统监控信息 状态
            clean_task_obj.enabled = True if enabled == "1" else False
            clean_task_obj.save()
        # 更新保留天数
        if save_days and config_obj:
            config_obj.configValue = save_days
            config_obj.save()
        # 更新监控获取频率
        if interval:
            periodictask_obj.interval.every = interval
            periodictask_obj.interval.save()
        return SuccessResponse(data={
            "enabled": periodictask_obj.enabled,
            "interval": periodictask_obj.interval.every,
            "save_days": config_obj.configValue if config_obj else "30",
        })

    def clean_all(self, request: Request, *args, **kwargs):
        """
        清空监控信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.get_queryset().delete()
        return SuccessResponse(msg="清空成功")
