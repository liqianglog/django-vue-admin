import django_filters

from apps.permission.models import Menu


class MenuFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Menu
        fields = '__all__'
