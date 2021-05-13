import request from '@/utils/request'

// 查询项目列表
export function listProject(query) {
  return request({
    url: '/project/project/',
    method: 'get',
    params: query
  })
}

// 查询项目详细
export function getProject(projectId) {
  return request({
    url: '/project/project/' + projectId + '/',
    method: 'get'
  })
}

// 新增项目
export function addProject(data) {
  return request({
    url: '/project/project/',
    method: 'post',
    data: data
  })
}

// 修改项目
export function updateProject(data) {
  return request({
    url: '/project/project/' + data.id + '/',
    method: 'put',
    data: data
  })
}

// 删除项目
export function delProject(projectId) {
  return request({
    url: '/project/project/' + projectId + '/',
    method: 'delete'
  })
}

// 导出项目
export function exportProject(query) {
  return request({
    url: '/project/project/export/',
    method: 'get',
    params: query
  })
}

// 下载项目导入模板
export function importTemplate() {
  return request({
    url: '/project/project/importTemplate/',
    method: 'get'
  })
}

// 项目导入
export function importsProject(data) {
  return request({
    url: '/project/project/importTemplate/',
    method: 'post',
    data: data
  })
}
