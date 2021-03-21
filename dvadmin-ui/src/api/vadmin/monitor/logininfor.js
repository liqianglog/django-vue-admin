import request from '@/utils/request'

// 查询登录日志列表
export function list(query) {
  return request({
    url: '/admin/system/logininfor/',
    method: 'get',
    params: query
  })
}

// 删除登录日志
export function delLogininfor(infoId) {
  return request({
    url: `/admin/system/logininfor/${infoId}/`,
    method: 'delete'
  })
}

// 清空登录日志
export function cleanLogininfor() {
  return request({
    url: '/admin/system/logininfor/clean',
    method: 'delete'
  })
}

// 导出登录日志
export function exportLogininfor(query) {
  return request({
    url: '/admin/system/logininfor/export',
    method: 'get',
    params: query
  })
}
