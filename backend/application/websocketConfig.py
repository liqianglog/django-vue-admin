# -*- coding: utf-8 -*-
import django

django.setup()
import json
import urllib

#处理websocket传参
from jwt import InvalidSignatureError

from application import settings
from dvadmin.system.models import MessageCenter


def request_data(scope):
    query_string = scope.get('query_string', b'').decode('utf-8')
    qs = urllib.parse.parse_qs(query_string)
    return qs


# 全部的websocket sender
CONNECTIONS = {}


# 判断用户是否已经连接
def check_connection(key):
    return key in CONNECTIONS


# 发送消息结构体
def message(sender, msg_type, msg):
    text = json.dumps({
        'sender': sender,
        'contentType': msg_type,
        'content': msg,
    })
    return {
        'type': 'websocket.send',
        'text': text
    }


async def websocket_application(scope, receive, send):
    while True:
        event = await receive()
        # print('[event] ', event)
        qs = request_data(scope)
        print(1,qs)
        auth = qs.get('auth', [''])[0]
        user_id = None
        # 收到建立WebSocket连接的消息
        if event['type'] == 'websocket.connect':
            # 昵称验证
            if not auth:
                break
            else:
                try:
                    import jwt
                    decoded_result = jwt.decode(auth, settings.SECRET_KEY, algorithms=["HS256"])
                    if decoded_result:
                        user_id = decoded_result.get('user_id')
                        # 记录
                        CONNECTIONS[user_id] = send
                except InvalidSignatureError:
                    break
            if auth in CONNECTIONS:
                break

            await send({'type': 'websocket.accept'})
            await send(message('system', 'INFO', '连接成功'))
            # # 发送好友列表
            # friends_list = list(CONNECTIONS.keys())
            # await send(message('system', 'INFO', friends_list))
            #
            # # 向其他人群发消息, 有人登录了
            # for other in CONNECTIONS.values():
            #     await other(message('system', 'addFriend', auth))


        # 收到中断WebSocket连接的消息
        elif event['type'] == 'websocket.disconnect':
            # 移除记录
            if user_id in CONNECTIONS:
                CONNECTIONS.pop(user_id)

            # # 向其他人群发消息, 有人离线了
            # for other in CONNECTIONS.values():
            #     await other(message('system', 'removeFriend', user_id))

        # 其他情况,正常的WebSocket消息
        elif event['type'] == 'websocket.receive':
            print(11,event)
            if event['text'] == 'ping':
                await send(message('system', 'text', 'pong!'))
            else:
                receive_msg = json.loads(event['text'])
                message_id = receive_msg.get('message_id', None)
                _MessageCenter = MessageCenter.objects.filter(id=message_id).first()
                if _MessageCenter:
                    user_list = _MessageCenter.target_user.values_list('id',flat=True)
                    for send_user in user_list:
                        if send_user in CONNECTIONS:
                            content_type = receive_msg.get('contentType', 'TEXT')
                            content = receive_msg.get('content', '')
                            msg = message(user_id, content_type, content)
                            await CONNECTIONS[send_user](msg)
                        else:
                            msg = message('system', 'text', '对方已下线或不存在')
                            await send(msg)
        else:
            print('a1a1a1')
            pass

    print('[disconnect]')