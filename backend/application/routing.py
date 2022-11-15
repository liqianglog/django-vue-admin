# -*- coding: utf-8 -*-
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.urls import path

from application.websocketConfig import MegCenter

websocket_urlpatterns = [
    path('ws/<str:service_uid>/', MegCenter.as_asgi()), #consumers.DvadminWebSocket 是该路由的消费者
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns #指明路由文件是devops/routing.py
        )
    ),
})