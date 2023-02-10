import { downloadFile, request } from '@/api/service'

export const urlPrefix = '/api/carton/verify_manage/back_haul_file/'

export function GetList (query) {
  return request({
    url: urlPrefix,
    method: 'get',
    params: query
  })
}

export function GetObj (obj) {
  return request({
    url: urlPrefix + obj.id + '/',
    method: 'get'
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

/***
 * 文件下载
 * @param params
 * @constructor
 */
export function Download (params) {
  return downloadFile({
    url: urlPrefix + params.id + '/download_file/',
    params: {},
    method: 'get',
    filename: `工单${params.production_work_no}回传文件`
  })
}
