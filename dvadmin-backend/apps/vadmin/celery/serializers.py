from django_celery_beat.models import IntervalSchedule, CrontabSchedule, PeriodicTask
from rest_framework import serializers

from apps.vadmin.op_drf.serializers import CustomModelSerializer
from apps.vadmin.utils.exceptions import APIException


class IntervalScheduleSerializer(CustomModelSerializer):
    class Meta:
        model = IntervalSchedule
        fields = '__all__'


class CrontabScheduleSerializer(CustomModelSerializer):

    def save(self, **kwargs):
        queryset = CrontabSchedule.objects.filter(**self.validated_data)
        if queryset.count() and (
                queryset.count() == 1 and self.initial_data.get('id', None) not in queryset.values_list('id',
                                                                                                        flat=True)):
            raise APIException(message='值已存在!!!')
        super().save(**kwargs)

    class Meta:
        model = CrontabSchedule
        exclude = ('timezone',)


class PeriodicTaskSerializer(CustomModelSerializer):
    interval_list = serializers.SerializerMethodField(read_only=True)
    crontab_list = serializers.SerializerMethodField(read_only=True)

    def get_interval_list(self, obj):
        return IntervalScheduleSerializer(obj.interval).data if obj.interval else {}

    def get_crontab_list(self, obj):
        return CrontabScheduleSerializer(obj.crontab).data if obj.crontab else {}

    class Meta:
        model = PeriodicTask
        fields = '__all__'
