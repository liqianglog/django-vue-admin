import django_filters
from django_celery_beat.models import IntervalSchedule, CrontabSchedule, PeriodicTask


class IntervalScheduleFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = IntervalSchedule
        fields = '__all__'


class CrontabScheduleFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = CrontabSchedule
        exclude = ('timezone',)


class PeriodicTaskFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = PeriodicTask
        fields = '__all__'

