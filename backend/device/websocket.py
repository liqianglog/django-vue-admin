import json
from hashlib import md5
from datetime import datetime

import jwt
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from application.websocketConfig import set_message


class DeviceStatusWebSocket(AsyncJsonWebsocketConsumer):
    """设备状态ws"""
    chat_group = 'device_status'

    async def connect(self):
        try:
            print('设备ws创建连接', self.scope)
            self.token = self.scope['url_route']['kwargs']['token']
            decoded_result = jwt.decode(self.token, settings.SECRET_KEY, algorithms=['HS256'])
            if decoded_result:
                self.uid = decoded_result.get('user_id')
                self.hash = md5(str(self.token).encode('utf-8'))
                self.chat_name = f'{self.chat_group}:user_{self.uid}'
                await self.channel_layer.group_add(self.chat_name, self.channel_name)
                await self.accept()
            else:
                raise jwt.InvalidSignatureError()
        except jwt.InvalidSignatureError:
            await self.send_json(set_message('system', 'SYSTEM', {'message': 'Token无效'}), True)
            await self.disconnect(None)
        except jwt.ExpiredSignatureError:
            await self.send_json(set_message('system', 'SYSTEM', {'message': 'Token过期'}), True)
            await self.disconnect(None)

    async def disconnect(self, code):
        print('设备ws连接关闭')
        await self.channel_layer.group_discard(self.chat_name, self.channel_name)
        try:
            await self.close(code)
        except:
            pass
