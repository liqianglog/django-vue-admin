/*
 * @创建文件时间: 2021-06-01 22:41:21
 * @Auther: 猿小天
 * @最后修改人: 猿小天
 * @最后修改时间: 2021-07-04 22:39:11
 * 联系Qq:1638245306
 * @文件介绍: 权限管理接口
 */
import { request } from '@/api/service'

export const urlPrefix = '/api/system/button/'

export function GetList (query) {
  return request({
    url: urlPrefix,
    method: 'get',
    data: query
  })
}
export function createObj (obj) {
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
    method: 'delete',
    data: { id }
  })
}
