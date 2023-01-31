# -*- coding: utf-8 -*-
from django.conf.urls import re_path
from rest_framework import routers

from .views.crontab_schedule import CrontabScheduleModelViewSet
from .views.interval_schedule import IntervalScheduleModelViewSet
from .views.periodic_task import PeriodicTaskModelViewSet

router = routers.SimpleRouter()
# 调度间隔
router.register(r'intervalschedule', IntervalScheduleModelViewSet)
router.register(r'crontabschedule', CrontabScheduleModelViewSet)
router.register(r'periodictask', PeriodicTaskModelViewSet)
urlpatterns = [
    re_path(r'^tasks_as_choices/', PeriodicTaskModelViewSet.as_view({'get': 'tasks_as_choices'})),
    re_path(r'^operate_celery/', PeriodicTaskModelViewSet.as_view({'post': 'operate_celery'})),
]
urlpatterns += router.urls
