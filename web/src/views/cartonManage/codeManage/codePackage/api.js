
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
    url: urlPrefix,
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
 * 创建订单
 */
export function createOrder (obj) {
  return request({
    url: urlPrefix + 'create_order/',
    method: 'post',
    data: obj
  })
}

/**
 * 获取码包详情
 */
export function getCodePackage (params) {
  return request({
    url: 'api/production/code_package/',
    method: 'get',
    params: params
  })
}

/**
 * 获取导入报告
 * @param {*} params
 * @returns
 */
export function getExportReport (params) {
  return request({
    url: urlPrefix + 'export_report/' + params.id + '/',
    method: 'get'
  })
}

/**
 * 数据归档
 * @param {*} params
 * @returns
 */
export function placeOnFile (params) {
  return request({
    url: urlPrefix + 'place_on_file/' + params.id + '/',
    method: 'post'
  })
}
