import ElementUI from 'element-ui'
import util from '@/libs/util'
function initWebSocket (e) {
  const token = util.cookies.get('token')
  if (token) {
    const wsUri = process.env.VUE_APP_WEBSOCKET + '/ws/' + token + '/?room=message_center'
    this.socket = new WebSocket(wsUri)// 这里面的this都指向vue
    this.socket.onerror = webSocketOnError
    this.socket.onmessage = webSocketOnMessage
    this.socket.onclose = closeWebsocket
  }
}

function webSocketOnError (e) {
  ElementUI.Notification({
    title: '',
    message: 'WebSocket连接发生错误' + JSON.stringify(e),
    type: 'error',
    position: 'bottom-right',
    duration: 3000
  })
}
function webSocketOnMessage (e) {
  const data = JSON.parse(e.data)
  if (data.contentType === 'INFO') {
    ElementUI.Notification({
      title: 'websocket',
      message: data.content,
      type: 'success',
      position: 'bottom-right',
      duration: 3000
    })
  } else if (data.contentType === 'ERROR') {
    ElementUI.Notification({
      title: '',
      message: data.content,
      type: 'error',
      position: 'bottom-right',
      duration: 0
    })
  } else if (data.contentType === 'TEXT') {
    ElementUI.Notification({
      title: '温馨提示',
      message: data.content,
      type: 'success',
      position: 'bottom-right',
      duration: 0
    })
  } else {
    console.log(data.content)
  }
}
// 关闭websiocket
function closeWebsocket () {
  console.log('连接已关闭...')
  // close()
  this.socket.close()
}

function webSocketSend (message) {
  this.socket.send(JSON.stringify(message))
}
export default {
  initWebSocket, closeWebsocket, webSocketSend
}
