import { d2CrudPlus } from 'd2-crud-plus'
import group from './group'

function install (Vue, options) {
  Vue.component('foreign-key-crud-form', () => import('./foreign-key-crud-form'))
  if (d2CrudPlus != null) {
    // 注册字段类型`demo-extend`
    d2CrudPlus.util.columnResolve.addTypes(group)
  }
}

// 导出install， 通过`vue.use(D2pDemoExtend)`安装后 ，`demo-extend` 就可以在`crud.js`中使用了
export default {
  install
}
