# -*- coding: utf-8 -*-
import urllib

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer
import json

from jwt import InvalidSignatureError

from application import settings
from dvadmin.system.models import MessageCenter

send_dict = {}

# 发送消息结构体
def message(sender, msg_type, msg):
    text = {
        'sender': sender,
        'contentType': msg_type,
        'content': msg,
    }
    return text

#异步获取消息中心的目标用户
@database_sync_to_async
def _get_message_center_instance(message_id):
    _MessageCenter = MessageCenter.objects.filter(id=message_id).values_list('target_user',flat=True)
    if _MessageCenter:
        return _MessageCenter
    else:
        return []


def request_data(scope):
    query_string = scope.get('query_string', b'').decode('utf-8')
    qs = urllib.parse.parse_qs(query_string)
    return qs

class DvadminWebSocket(AsyncJsonWebsocketConsumer):
    async def connect(self):
        try:
            import jwt
            self.service_uid = self.scope["url_route"]["kwargs"]["service_uid"]
            params = request_data(self.scope)
            room = params.get('room')[0]
            decoded_result = jwt.decode(self.service_uid, settings.SECRET_KEY, algorithms=["HS256"])
            if decoded_result:
                self.user_id = decoded_result.get('user_id')
                self.chat_group_name = room
                #收到连接时候处理，
                await self.channel_layer.group_add(
                    self.chat_group_name,
                    self.channel_name
                )
                # 将该客户端的信息发送函数与客户端的唯一身份标识绑定，保存至自定义的字典中
                if len(send_dict)==0:
                    send_dict.setdefault(self.chat_group_name, {})
                for room in send_dict.keys():
                    if room == self.chat_group_name:
                        send_dict[self.chat_group_name][self.user_id] = self.send
                    else:
                        send_dict.setdefault(self.chat_group_name,{})
                await self.accept()
                await self.send_json(message('system', 'INFO', '连接成功'))
        except InvalidSignatureError:
            await self.disconnect(None)


    async def disconnect(self, close_code):
        # 删除 send_dict 中对应的信息
        del send_dict[self.chat_group_name][self.user_id]
        # Leave room group
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)
        print("连接关闭")
        await self.close(close_code)

    async def receive(self, text_data=None, byte_text_data=None):
        print(text_data)
        try:
            text_data_json = json.loads(text_data)
        except Exception as e:
            print('数据无法被json格式化', e)
            await self.disconnect(400)
        else:
            print(123,text_data_json)
            # 获取将要推送信息的目标身份标识，调用保存在 send_dict中的信息发送函数
            message_id = text_data_json.get('message_id', None)
            user_list = await _get_message_center_instance(message_id)
            for send_user in user_list:
                await send_dict[self.chat_group_name][send_user](text_data=json.dumps(text_data_json))