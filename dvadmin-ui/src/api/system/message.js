import request from '@/utils/request'

// 查询参数列表
export function listMessage(query) {
  return request({
    url: '/system/message/',
    method: 'get',
    params: query
  })
}

// 查询参数详细
export function getMessage(messageId) {
  return request({
    url: '/system/message/' + messageId + '/',
    method: 'get'
  })
}

// 新增参数配置
export function addMessage(data) {
  return request({
    url: '/system/message/',
    method: 'post',
    data: data
  })
}

// 修改参数配置
export function updateMessage(data) {
  return request({
    url: '/system/message/' + data.id + '/',
    method: 'put',
    data: data
  })
}

// 删除参数配置
export function delMessage(messageId) {
  return request({
    url: '/system/message/' + messageId + '/',
    method: 'delete'
  })
}


// 导出参数
export function exportMessage(query) {
  return request({
    url: '/system/message/export/',
    method: 'get',
    params: query
  })
}
