import request from '@/utils/request'

// 查询服务器信息详细
export function getServerList(params) {
  return request({
    url: 'admin/monitor/server/',
    params,
    method: 'get'
  })
}

// 修改服务器信息
export function updateServerInfo(id, data) {
  let {name, remark} = data;
  return request({
    url: `admin/monitor/server/${id}/`,
    data: {
      name,
      remark
    },
    method: 'PUT'
  })
}

// 获取监控配置信息
export function getMonitorStatusInfo() {
  return request({
    url: 'admin/monitor/monitor/enabled/',
    method: 'get'
  })
}

// 更新监控配置信息
export function updateMonitorStatusInfo(params) {
  return request({
    url: 'admin/monitor/monitor/enabled/',
    params,
    method: 'get'
  })
}

// 清空记录
export function cleanMonitorLog() {
  return request({
    url: 'admin/monitor/monitor/clean/',
    method: 'delete'
  })
}

// 获取监控记录
export function getMonitorLogs(id, params) {
  return request({
    url: `admin/monitor/monitor/rate/${id}/`,
    params,
    method: 'get'
  })
}

// 获取服务器最新监控日志信息
export function getServerLatestLog(id) {
  return request({
    url: `admin/monitor/monitor/info/${id}/`,
    method: 'get'
  })
}
