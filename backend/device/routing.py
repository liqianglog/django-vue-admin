from django.urls import path
from device.websocket import DeviceStatusWebSocket

websocket_urlpatterns = [
    path('ws/gateway_status/<str:token>/', DeviceStatusWebSocket.as_asgi()),
]
