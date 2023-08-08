# -*- coding: utf-8 -*-
from django.urls import path
from application.websocketConfig import MegCenter
from device.routing import websocket_urlpatterns as device_ws_url

websocket_urlpatterns = [
    path('ws/<str:service_uid>/', MegCenter.as_asgi()),  # consumers.DvadminWebSocket 是该路由的消费者
    *device_ws_url,
]
