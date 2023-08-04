import { request } from '/@/utils/service';
import { PageQuery } from './types'

export function getRoleList(query: PageQuery) {
  return request({
    url: '/api/system/role/',
    method: 'get',
    params: query,
  });
}

export function getModelList() {
  return request({
    url: '/api/system/column/get_models/',
    method: 'get',
  });
}