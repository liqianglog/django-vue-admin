import request from '@/utils/request'
/**
 * 封装celery任务信息接口请求
 */
// 获取
export const sync_data_prefix = '/admin/celery';

// 获取
export function getIntervalschedulea(id) {
  return request({
    url: `${sync_data_prefix}/intervalschedule/${id}/`,
    method: 'get'
  });
}

// 获取
export function listIntervalschedule(params) {
  return request({
    url: `${sync_data_prefix}/intervalschedule/`,
    method: 'get',
    params
  });
}

// 更新
export function updateIntervalschedule(data) {
  return request({
    url: `${sync_data_prefix}/intervalschedule/${data.id}/`,
    method: 'put',
    data
  });
}
// 新增
export function createIntervalschedule(data) {
  return request({
    url: `${sync_data_prefix}/intervalschedule/`,
    method: 'post',
    data
  });
}
// 删除
export function deleteIntervalschedule(id) {
  return request({
    url: `${sync_data_prefix}/intervalschedule/${id}/`,
    method: 'delete'
  });
}

// 获取
export function getCrontabSchedule(id) {
  return request({
    url: `${sync_data_prefix}/crontabschedule/${id}/`,
    method: 'get'
  });
}

// 获取
export function listCrontabSchedule(params) {
  return request({
    url: `${sync_data_prefix}/crontabschedule/`,
    method: 'get',
    params
  });
}

// 更新
export function updateCrontabSchedule(data) {
  return request({
    url: `${sync_data_prefix}/crontabschedule/${data.id}/`,
    method: 'put',
    data
  });
}
// 新增
export function createCrontabSchedule(data) {
  return request({
    url: `${sync_data_prefix}/crontabschedule/`,
    method: 'post',
    data
  });
}
// 删除
export function deleteCrontabSchedule(id) {
  return request({
    url: `${sync_data_prefix}/crontabschedule/${id}/`,
    method: 'delete'
  });
}

// 获取
export function getPeriodicTask(id) {
  return request({
    url: `${sync_data_prefix}/periodictask/${id}/`,
    method: 'get'
  });
}

// 获取
export function listPeriodicTask(params) {
  return request({
    url: `${sync_data_prefix}/periodictask/`,
    method: 'get',
    params
  });
}
// 获取所有 tasks 名称
export function TasksAsChoices(params) {
  return request({
    url: `${sync_data_prefix}/tasks_as_choices/`,
    method: 'get',
    params
  });
}

// 更新
export function updatePeriodicTask(data) {
  return request({
    url: `${sync_data_prefix}/periodictask/${data.id}/`,
    method: 'put',
    data
  });
}
// 新增
export function createPeriodicTask(data) {
  return request({
    url: `${sync_data_prefix}/periodictask/`,
    method: 'post',
    data
  });
}
// 删除
export function deletePeriodicTask(id) {
  return request({
    url: `${sync_data_prefix}/periodictask/${id}/`,
    method: 'delete'
  });
}

// 获取
export function operatesyncdata(data) {
  return request({
    url: `${sync_data_prefix}/operate_celery/`,
    method: 'post',
    data
  });
}

// 查询定时任务日志列表
export function list(query) {
  return request({
    url: '/admin/system/celery_log/',
    method: 'get',
    params: query
  })
}

// 删除定时任务日志
export function delCeleryLog(infoId) {
  return request({
    url: `/admin/system/celery_log/${infoId}/`,
    method: 'delete'
  })
}

// 清空定时任务日志
export function cleanCeleryLog() {
  return request({
    url: '/admin/system/celery_log/clean',
    method: 'delete'
  })
}

// 导出定时任务日志
export function exportCeleryLog(query) {
  return request({
    url: '/admin/system/celery_log/export',
    method: 'get',
    params: query
  })
}
