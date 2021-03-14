/*
 * @Author: 庄志莹
 * @Date: 2021-03-08 19:39:35
 * @LastEditTime: 2021-03-08 20:03:36
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \dvadmin-ui\src\api\permission\msg.js
 */
import request from '@/utils/request'

// 查询消息列表
export function getList(query) {
  return request({
    url: '/admin/system/config/',
    method: 'get',
    params: query
  })
}

// 查看详情
export function getDesc(configId) {
  return request({
    url: '/admin/system/config/' + configId + '/',
    method: 'get'
  })
}

// // 根据消息标题查询
// export function getConfigKey(configKey) {
//   return request({
//     url: '/admin/system/config/configKey/' + configKey + '/',
//     method: 'get'
//   })
// }

// 新增消息
export function addMsg(data) {
  return request({
    url: '/admin/system/config/',
    method: 'post',
    data: data
  })
}

// 修改消息
export function updateMsg(data) {
  return request({
    url: '/admin/system/config/' + data.id + '/',
    method: 'put',
    data: data
  })
}

// 删除消息
export function delMsg(configId) {
  return request({
    url: '/admin/system/config/' + configId + '/',
    method: 'delete'
  })
}


// 导出消息
export function exportMsg(query) {
  return request({
    url: '/admin/system/config/export/',
    method: 'get',
    params: query
  })
}
