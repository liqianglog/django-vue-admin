
import { request } from '@/api/service'
export const urlPrefix = 'api/carton/code_manage/code_package/'

export function GetList (query) {
  return request({
    url: urlPrefix,
    method: 'get',
    params: query
  })
}

/**
 * 获取单例
 */
export function getObj (params) {
  return request({
    url: urlPrefix + params.id + '/',
    method: 'get',
    params: params
  })
}

export function AddObj (obj) {
  return request({
    url: urlPrefix + 'create_code_package_info/',
    method: 'post',
    data: obj
  })
}

export function UpdateObj (obj) {
  return request({
    url: urlPrefix + obj.id + '/',
    method: 'put',
    data: obj
  })
}
export function DelObj (id) {
  return request({
    url: urlPrefix + id + '/',
    method: 'delete'
  })
}

/**
 * 查看日志
 * @param params
 * @returns {*}
 */
export function viewLog (params) {
  return request({
    url: urlPrefix + params.id + '/view_log/',
    method: 'get',
    params: params
  })
}


/**
 * 获取导入报告
 * @param {*} params
 * @returns
 */
export function getImportReport (params) {
  return request({
    url: urlPrefix + params.id + '/import_report/',
    method: 'get'
  })
}
