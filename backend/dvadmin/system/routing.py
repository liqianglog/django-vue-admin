# -*- coding: utf-8 -*-
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/<str:service_uid>/', consumers.DvadminWebSocket.as_asgi()), #consumers.DvadminWebSocket 是该路由的消费者
]