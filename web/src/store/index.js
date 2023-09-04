import Vue from 'vue'
import Vuex from 'vuex'

import d2admin from './modules/d2admin'
import { getStoreModules } from '@/views/plugins'
Vue.use(Vuex)
// 创建一个空的modules对象
const modules = { d2admin: d2admin }
Object.assign(modules, getStoreModules())
export default new Vuex.Store({
  modules
})
