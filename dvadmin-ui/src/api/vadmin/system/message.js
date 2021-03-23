import request from '@/utils/request'

// 查询通知列表
export function listMessage(query) {
  return request({
    url: '/admin/system/message/',
    method: 'get',
    params: query
  })
}

// 查询通知详细
export function getMessage(messageId) {
  return request({
    url: '/admin/system/message/' + messageId + '/',
    method: 'get'
  })
}

// 新增通知配置
export function addMessage(data) {
  return request({
    url: '/admin/system/message/',
    method: 'post',
    data: data
  })
}

// 修改通知配置
export function updateMessage(data) {
  return request({
    url: '/admin/system/message/' + data.id + '/',
    method: 'put',
    data: data
  })
}

// 删除通知配置
export function delMessage(messageId) {
  return request({
    url: '/admin/system/message/' + messageId + '/',
    method: 'delete'
  })
}


// 导出通知
export function exportMessage(query) {
  return request({
    url: '/admin/system/message/export/',
    method: 'get',
    params: query
  })
}

// 获取用户通知列表
export function userMessage(query) {
  return request({
    url: '/admin/system/message/user_messages/',
    method: 'get',
    params: query
  })
}

// 修改通知为已读
export function updateIsRead(data) {
  return request({
    url: '/admin/system/message/is_read/'+ data.id + '/',
    method: 'put',
  })
}
