/*
 * @创建文件时间: 2021-06-02 10:33:33
 * @Auther: 猿小天
 * @最后修改人: 猿小天
 * @最后修改时间: 2021-08-12 22:53:38
 * 联系Qq:1638245306
 * @文件介绍: 登录的接口
 */

import { request } from '@/api/service'

export function SYS_USER_LOGIN (data) {
  return request({
    url: 'api/login/',
    method: 'post',
    data
  })
}

export function SYS_USER_LOGOUT (data) {
  return request({
    url: 'api/logout/',
    method: 'post',
    data
  })
}

export function getCaptcha () {
  return request({
    url: 'api/captcha/',
    method: 'get'
  })
}
