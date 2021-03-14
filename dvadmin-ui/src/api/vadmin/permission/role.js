import request from '@/utils/request'

// 查询角色列表
export function listRole(query) {
  return request({
    url: '/admin/permission/role/',
    method: 'get',
    params: query
  })
}

// 查询角色详细
export function getRole(roleId) {
  return request({
    url: '/admin/permission/role/' + roleId + '/',
    method: 'get'
  })
}

// 新增角色
export function addRole(data) {
  return request({
    url: '/admin/permission/role/',
    method: 'post',
    data: data
  })
}

// 修改角色
export function updateRole(data) {
  return request({
    url: '/admin/permission/role/' + data.id + '/',
    method: 'put',
    data: data
  })
}

// 角色数据权限
export function dataScope(data) {
  return request({
    url: '/admin/permission/role/' + data.id + '/',
    method: 'put',
    data: data
  })
}

// 角色状态修改
export function changeRoleStatus(roleId, status) {
  const data = {
    roleId,
    status
  }
  return request({
    url: '/admin/permission/role/changeStatus/',
    method: 'put',
    data: data
  })
}

// 删除角色
export function delRole(roleId) {
  return request({
    url: '/admin/permission/role/' + roleId + '/',
    method: 'delete'
  })
}

// 导出角色
export function exportRole(query) {
  return request({
    url: '/admin/permission/role/export/',
    method: 'get',
    params: query
  })
}
