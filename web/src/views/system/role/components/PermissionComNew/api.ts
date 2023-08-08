import { request } from "/@/utils/service";

export function getDataPermissionRange() {
  return request({
    url: '/api/system/role_menu_button_permission/data_scope/',
    method: 'get',
  })
}
export function getDataPermissionDept() {
  return request({
    url: '/api/system/role_menu_button_permission/role_to_dept_all/',
    method: 'get'
  })
}

export function getDataPermissionMenu() {
  return request({
    url: '/api/system/role_menu_button_permission/get_role_permissions/',
    method: 'get'
  })
}