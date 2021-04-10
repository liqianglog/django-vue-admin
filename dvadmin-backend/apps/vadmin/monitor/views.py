from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
from rest_framework.request import Request

from .filters import ServerFilter, MonitorFilter
from .models import Server, Monitor
from .serializers import ServerSerializer, MonitorSerializer
from ..op_drf.response import SuccessResponse
from ..op_drf.viewsets import CustomModelViewSet
from ..permission.permissions import CommonPermission
from ..system.models import ConfigSettings


class ServerModelViewSet(CustomModelViewSet):
    """
    服务器信息 模型的CRUD视图
    """
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
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

    def get_monitor_info(self, request: Request, *args, **kwargs):
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

        # 获取保留天数
        return SuccessResponse(data={
            "enabled": periodictask_obj.enabled,
            "interval": periodictask_obj.interval.every,
            "save_days": config_obj.configValue if config_obj else "30",
        })

    def enabled_monitor_info(self, request: Request, *args, **kwargs):
        enabled = request.query_params.get('enabled', None)
        save_days = request.query_params.get('save_days', None)
        interval = request.query_params.get('interval', None)

        periodictask_obj = PeriodicTask.objects.filter(task='apps.vadmin.monitor.tasks.get_monitor_info').first()
        if enabled:
            # 更新监控状态
            periodictask_obj.enabled = True if enabled == "1" else False
            periodictask_obj.save()

            # 更新 定时清理多余 系统监控信息 状态
            clean_task_obj = PeriodicTask.objects.filter(
                task='apps.vadmin.monitor.tasks.clean_surplus_monitor_info').first()
            clean_task_obj.enabled = True if enabled == "1" else False
            clean_task_obj.save()
        # 更新保留天数
        config_obj = ConfigSettings.objects.filter(configKey='sys.monitor.info.save_days').first()
        print(33, save_days)
        print(22, config_obj)
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
