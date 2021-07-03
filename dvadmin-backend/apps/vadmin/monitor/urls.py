from django.urls import re_path
from rest_framework.routers import DefaultRouter

from apps.vadmin.monitor.views import ServerModelViewSet, MonitorModelViewSet

router = DefaultRouter()
router.register(r'server', ServerModelViewSet)
router.register(r'monitor', MonitorModelViewSet)

urlpatterns = [
    re_path('monitor/info/(?P<pk>.*)/', MonitorModelViewSet.as_view({'get': 'get_monitor_info'})),
    re_path('monitor/rate/(?P<pk>.*)/', MonitorModelViewSet.as_view({'get': 'get_rate_info'})),
    re_path('monitor/enabled/', MonitorModelViewSet.as_view({'get': 'enabled_monitor_info'})),
    re_path('monitor/clean/', MonitorModelViewSet.as_view({'get': 'clean_all'})),
]
urlpatterns += router.urls
