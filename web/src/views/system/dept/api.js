import { request } from '@/api/service'
export const urlPrefix = '/api/system/dept/'

/**
 * 列表查询
 */
export function GetList (query) {
  // query.limit = 999;
  return request({
    url: urlPrefix,
    method: 'get',
    params: query
  })
}

/**
 * 新增
 */
export function createObj (obj) {
  return request({
    url: urlPrefix,
    method: 'post',
    data: obj
  })
}

/**
 * 修改
 */
export function UpdateObj (obj) {
  return request({
    url: urlPrefix + obj.id + '/',
    method: 'put',
    data: obj
  })
}

/**
 * 删除
 */
export function DelObj (id) {
  return request({
    url: urlPrefix + id + '/',
    method: 'delete',
    data: { id }
  })
}

/**
 * 部门懒加载
 */
export function DeptLazy (query) {
  return request({
    url: '/api/system/dept_lazy_tree/',
    method: 'get',
    params: query
  })
}
