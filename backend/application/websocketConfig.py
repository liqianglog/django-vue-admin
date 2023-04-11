# -*- coding: utf-8 -*-
import urllib

from asgiref.sync import sync_to_async, async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer
import json

from channels.layers import get_channel_layer
from jwt import InvalidSignatureError
from rest_framework.request import Request

from application import settings

send_dict = {}


# 发送消息结构体
def set_message(sender, msg_type, msg, refresh_unread=False):
    text = {
        'sender': sender,
        'contentType': msg_type,
        'content': msg,
        'refresh_unread': refresh_unread
    }
    return text


# 异步获取消息中心的目标用户
@database_sync_to_async
def _get_message_center_instance(message_id):
    from dvadmin.system.models import MessageCenter
    _MessageCenter = MessageCenter.objects.filter(id=message_id).values_list('target_user', flat=True)
    if _MessageCenter:
        return _MessageCenter
    else:
        return []


@database_sync_to_async
def _get_message_unread(user_id):
    """获取用户的未读消息数量"""
    from dvadmin.system.models import MessageCenterTargetUser
    count = MessageCenterTargetUser.objects.filter(users=user_id, is_read=False).count()
    return count or 0


def request_data(scope):
    query_string = scope.get('query_string', b'').decode('utf-8')
    qs = urllib.parse.parse_qs(query_string)
    return qs


class DvadminWebSocket(AsyncJsonWebsocketConsumer):
    async def connect(self):
        try:
            import jwt
            self.service_uid = self.scope["url_route"]["kwargs"]["service_uid"]
            decoded_result = jwt.decode(self.service_uid, settings.SECRET_KEY, algorithms=["HS256"])
            if decoded_result:
                self.user_id = decoded_result.get('user_id')
                self.room_name = "user_" + str(self.user_id)
                # 收到连接时候处理，
                await self.channel_layer.group_add(
                    "dvadmin",
                    self.channel_name
                )
                await self.channel_layer.group_add(
                    self.room_name,
                    self.channel_name
                )
                await self.accept()
                # 主动推送消息
                unread_count = await _get_message_unread(self.user_id)
                if unread_count == 0:
                    # 发送连接成功
                    await self.send_json(set_message('system', 'SYSTEM', '连接成功'))
                else:
                    await self.send_json(
                        set_message('system', 'SYSTEM', "请查看您的未读消息~",
                                    refresh_unread=True))
        except InvalidSignatureError:
            await self.disconnect(None)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        await self.channel_layer.group_discard("dvadmin", self.channel_name)
        print("连接关闭")
        try:
            await self.close(close_code)
        except Exception:
            pass


class MegCenter(DvadminWebSocket):
    """
    消息中心
    """

    async def receive(self, text_data):
        # 接受客户端的信息，你处理的函数
        text_data_json = json.loads(text_data)
        # message_id = text_data_json.get('message_id', None)
        # user_list = await _get_message_center_instance(message_id)
        # for send_user in user_list:
        #     await self.channel_layer.group_send(
        #         "user_" + str(send_user),
        #         {'type': 'push.message', 'json': text_data_json}
        #     )

    async def push_message(self, event):
        """消息发送"""
        message = event['json']
        await self.send(text_data=json.dumps(message))



def websocket_push(room_name,message):
    """
    主动推送
    @param room_name: 群组名称
    @param message: 消息内容
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        room_name,
        {
            "type": "push.message",
            "json": message
        }
    )
