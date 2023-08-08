from django.urls import path
from rest_framework import routers

from device.views.gateway import GatewayViewSet
from device.views.template import TemplateViewSet, TemplateDetailViewSet
from device.views.terminal import TerminalViewSet


device_url = routers.SimpleRouter()
device_url.register(r'gateway', GatewayViewSet)
device_url.register(r'template', TemplateViewSet)
device_url.register(r'template_detail', TemplateDetailViewSet)
device_url.register(r'terminal', TerminalViewSet)

urlpatterns = []
urlpatterns += device_url.urls
