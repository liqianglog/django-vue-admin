import {Notification} from 'element-plus'
import store from '@/store'
import {Session} from "/@/utils/storage";
import {getWsBaseURL} from "/@/utils/baseUrl";

let socket=null;
function initWebSocket () {
    const token = Session.get('token');
    if (token) {
        const wsUri = getWsBaseURL() + 'ws/' + token + '/'
        this.socket = new WebSocket(wsUri)// 这里面的this都指向vue
        this.socket.onerror = webSocketOnError
        this.socket.onmessage = webSocketOnMessage
        this.socket.onclose = closeWebsocket
    }
}

function webSocketOnError (e) {
    Notification({
        title: '',
        message: 'WebSocket连接发生错误' + JSON.stringify(e),
        type: 'error',
        position: 'bottom-right',
        duration: 3000
    })
}

/**
 * 接收消息
 * @param e
 * @returns {any}
 */
function webSocketOnMessage (e) {
    const data = JSON.parse(e.data)
    const { unread } = data
    store.dispatch('d2admin/messagecenter/setUnread', unread || 0)
    if (data.contentType === 'SYSTEM') {
        Notification({
            title: '系统消息',
            message: data.content,
            type: 'success',
            position: 'bottom-right',
            duration: 3000
        })
    } else if (data.contentType === 'ERROR') {
        Notification({
            title: '',
            message: data.content,
            type: 'error',
            position: 'bottom-right',
            duration: 0
        })
    } else if (data.contentType === 'INFO') {
        Notification({
            title: '温馨提示',
            message: data.content,
            type: 'success',
            position: 'bottom-right',
            duration: 0
        })
    } else {
        Notification({
            title: '温馨提示',
            message: data.content,
            type: 'info',
            position: 'bottom-right',
            duration: 3000
        })
    }
}
// 关闭websiocket
function closeWebsocket () {
    console.log('连接已关闭...')
    Notification({
        title: 'websocket',
        message: '连接已关闭...',
        type: 'danger',
        position: 'bottom-right',
        duration: 3000
    })
}

/**
 * 发送消息
 * @param message
 */
function webSocketSend (message) {
    this.socket.send(JSON.stringify(message))
}
export default {
    initWebSocket, closeWebsocket, webSocketSend
}
