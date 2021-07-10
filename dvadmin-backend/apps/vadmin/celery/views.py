from django_celery_beat.admin import TaskSelectWidget
from django_celery_beat.models import IntervalSchedule, CrontabSchedule, PeriodicTask
from rest_framework.views import APIView

from apps.vadmin.celery.filters import IntervalScheduleFilter, CrontabScheduleFilter, PeriodicTaskFilter
from apps.vadmin.celery.serializers import IntervalScheduleSerializer, CrontabScheduleSerializer, PeriodicTaskSerializer
from apps.vadmin.op_drf.views import CustomAPIView
from apps.vadmin.op_drf.viewsets import CustomModelViewSet
from apps.vadmin.op_drf.response import SuccessResponse


class IntervalScheduleModelViewSet(CustomModelViewSet):
    """
    IntervalSchedule 调度间隔模型
    every 次数
    period 时间(天,小时,分钟,秒.毫秒)
    """
    queryset = IntervalSchedule.objects.all()
    serializer_class = IntervalScheduleSerializer
    create_serializer_class = IntervalScheduleSerializer
    update_serializer_class = IntervalScheduleSerializer
    filter_class = IntervalScheduleFilter
    search_fields = ('every', 'period')
    ordering = 'every'  # 默认排序


class CrontabScheduleModelViewSet(CustomModelViewSet):
    """
    CrontabSchedule crontab调度模型
    minute 分钟
    hour 小时
    day_of_week 每周的周几
    day_of_month 每月的某一天
    month_of_year 每年的某一个月

    """
    queryset = CrontabSchedule.objects.all()
    serializer_class = CrontabScheduleSerializer
    filter_class = CrontabScheduleFilter
    search_fields = ('minute', 'hour')
    ordering = 'minute'  # 默认排序


class PeriodicTaskModelViewSet(CustomModelViewSet):
    """
    PeriodicTask celery 任务数据模型
    name 名称
    task celery任务名称
    interval 频率
    crontab 任务编排
    args 形式参数
    kwargs 位置参数
    queue 队列名称
    exchange 交换
    routing_key 路由密钥
    expires 过期时间
    enabled 是否开启

    """
    queryset = PeriodicTask.objects.exclude(name="celery.backend_cleanup")
    serializer_class = PeriodicTaskSerializer
    filter_class = PeriodicTaskFilter
    search_fields = ('name', 'task', 'date_changed')
    ordering = 'date_changed'  # 默认排序


class TasksAsChoices(APIView):
    def get(self, request):
        """
        获取所有 tasks 名称
        :param request:
        :return:
        """
        lis = []

        def get_data(datas):
            for item in datas:
                if isinstance(item, (str, int)) and item:
                    lis.append(item)
                else:
                    get_data(item)

        get_data(TaskSelectWidget().tasks_as_choices())
        return SuccessResponse(list(set(lis)))


class OperateCeleryTask(CustomAPIView):
    def post(self, request):
        req_data = request.data
        task = req_data.get('celery_name', '')
        data = {
            'task': ''
        }
        test = f"""
from {'.'.join(task.split('.')[:-1])} import {task.split('.')[-1]}
task = {task.split('.')[-1]}.delay()
        """
        exec(test, data)
        return SuccessResponse({'task_id': data.get('task').id})
