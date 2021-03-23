from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from apps.vadmin.celery.views import IntervalScheduleModelViewSet, CrontabScheduleModelViewSet, PeriodicTaskModelViewSet, TasksAsChoices, \
    OperateCeleryTask

router = DefaultRouter()
# 调度间隔
router.register(r'intervalschedule', IntervalScheduleModelViewSet)
router.register(r'crontabschedule', CrontabScheduleModelViewSet)
router.register(r'periodictask', PeriodicTaskModelViewSet)

urlpatterns = format_suffix_patterns([
    # 获取所有 tasks 名称
    url(r'^tasks_as_choices/', TasksAsChoices.as_view()),
    url(r'^operate_celery/', OperateCeleryTask.as_view()),
])

urlpatterns += router.urls
