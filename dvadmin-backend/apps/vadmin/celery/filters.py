import django_filters
from djcelery.models import IntervalSchedule, CrontabSchedule, PeriodicTask


class IntervalScheduleFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = IntervalSchedule
        fields = '__all__'


class CrontabScheduleFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = CrontabSchedule
        fields = '__all__'


class PeriodicTaskFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = PeriodicTask
        fields = '__all__'

