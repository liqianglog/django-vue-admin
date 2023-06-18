import { d2CrudPlus } from 'd2-crud-plus'
import group from './group'

function install (Vue, options) {
  Vue.component('m2m-values-popover', () => import('./m2m-values-popover'))
  if (d2CrudPlus != null) {
    // 注册字段类型`demo-extend`
    d2CrudPlus.util.columnResolve.addTypes(group)
  }
}
// 导出install
export default {
  install
}
