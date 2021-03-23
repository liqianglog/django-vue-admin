import request from '@/utils/request'

// 查询操作日志列表
export function list(query) {
  return request({
    url: '/admin/system/operation_log/',
    method: 'get',
    params: query
  })
}

// 删除操作日志
export function delOperationLog(operId) {
  return request({
    url: '/admin/system/operation_log/' + operId + '/',
    method: 'delete'
  })
}

// 清空操作日志
export function cleanOperationLog() {
  return request({
    url: '/admin/system/operation_log/clean/',
    method: 'delete'
  })
}

// 导出操作日志
export function exportOperationLog(query) {
  return request({
    url: '/admin/system/operation_log/export/',
    method: 'get',
    params: query
  })
}
