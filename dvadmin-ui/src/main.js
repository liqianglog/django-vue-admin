import Vue from 'vue'

import Cookies from 'js-cookie'

import Element from 'element-ui'
import './assets/styles/element-variables.scss'

import '@/assets/styles/index.scss' // global css
import '@/assets/styles/ruoyi.scss' // ruoyi css
import App from './App'
import store from './store'
import router from './router'
import permission from './directive/permission'

import './assets/icons' // icon
import './permission' // permission control
import {getDicts} from "@/api/vadmin/system/dict/data";
import {getConfigKey} from "@/api/vadmin/system/config";
import {
  addDateRange,
  download,
  handleTree,
  parseTime,
  resetForm,
  selectDictLabel,
  selectDictDefault,
  selectDictLabels
} from "@/utils/ruoyi";
import Pagination from "@/components/Pagination";
// 自定义表格工具扩展
import RightToolbar from "@/components/RightToolbar"
import SmallDialog from '@/components/SmallDialog';
import DeptTree from '@/components/DeptTree';
import UsersTree from '@/components/UsersTree';
import ModelDisplay from '@/components/ModelDisplay';
import CommonIcon from '@/components/CommonIcon';
import CommonStaticTable from '@/components/CommonStaticTable';
import {getCrontabData, getIntervalData} from "./utils/validate"; // 通用图标组件

// 全局方法挂载
Vue.prototype.getDicts = getDicts
Vue.prototype.getConfigKey = getConfigKey
Vue.prototype.parseTime = parseTime
Vue.prototype.resetForm = resetForm
Vue.prototype.addDateRange = addDateRange
Vue.prototype.selectDictLabel = selectDictLabel
Vue.prototype.selectDictDefault = selectDictDefault
Vue.prototype.selectDictLabels = selectDictLabels
Vue.prototype.getCrontabData = getCrontabData
Vue.prototype.getIntervalData = getIntervalData
Vue.prototype.download = download
Vue.prototype.handleTree = handleTree
Vue.prototype.hasPermi = function (values) {
  const permissions = store.getters && store.getters.permissions
  return permissions.some(permission => {
    return "*:*:*" === permission || values.includes(permission)
  })
};

Vue.prototype.msgSuccess = function (msg) {
  this.$message({showClose: true, message: msg, type: "success"});
}

Vue.prototype.msgError = function (msg) {
  this.$message({showClose: true, message: msg, type: "error"});
}

Vue.prototype.msgInfo = function (msg) {
  this.$message.info(msg);
}
// 自定义组件
Vue.component('small-dialog', SmallDialog);
Vue.component('dept-tree', DeptTree);
Vue.component('users-tree', UsersTree);
Vue.component('model-display', ModelDisplay);
// 全局组件挂载
Vue.component('Pagination', Pagination)
Vue.component('RightToolbar', RightToolbar)
Vue.component('common-icon', CommonIcon);
Vue.component('common-static-table', CommonStaticTable);

Vue.use(permission)

/**
 * If you don't want to use mock-server
 * you want to use MockJs for mock api
 * you can execute: mockXHR()
 *
 * Currently MockJs will be used in the production environment,
 * please remove it before going online! ! !
 */

Vue.use(Element, {
  size: Cookies.get('size') || 'medium' // set element-ui default size
})

Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
