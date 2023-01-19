/*
 * @创建文件时间: 2021-08-02 23:56:15
 * @Auther: 猿小天
 * @最后修改人: 猿小天
 * @最后修改时间: 2021-08-21 15:09:18
 * 联系Qq:1638245306
 * @文件介绍:
 */
import { d2CrudPlus } from 'd2-crud-plus'
import group from './group'

export function install (Vue, options) {
  Vue.component('cron-selector-input', () => import('./cron-selector'))
  // Vue.component('d2p-row-format', () => import('./row'))
  if (d2CrudPlus != null) {
    // 注册字段类型`demo-extend`
    d2CrudPlus.util.columnResolve.addTypes(group)
  }
}

export default {
  install
}
