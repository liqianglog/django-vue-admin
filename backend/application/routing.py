# -*- coding: utf-8 -*-
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from dvadmin.system import routing as dvadminRouting


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            dvadminRouting.websocket_urlpatterns# 指明路由文件是devops/routing.py
        )
    ),
})