import { request } from '@/api/service'

export const urlPrefix = '/api/init/settings/'

// 系统配置
export default {
  namespaced: true,
  state: {
    siteName: '', // 网站名称
    siteLogo: '', // 网站logo地址
    loginBackground: '', // 登录页背景图
    loginBanner: '', // 登录页Banner图
    copyright: '', // 版权
    keepRecord: '' // 备案
  },
  actions: {
    /**
     * @description 请求最新配置
     * @param {Object} context
     */
    async init ({ state, dispatch, commit }) {
      // 请求配置
      request({
        url: urlPrefix,
        method: 'get'
      }).then(async res => {
        // 赋值
        await dispatch('d2admin/db/set', {
          dbName: 'sys',
          path: 'settings.init',
          value: res.data,
          user: true
        }, { root: true })
        dispatch('load')
      })
    },
    /**
     * @description 本地加载配置
     * @param {Object} context
     */
    async load ({ state, dispatch, commit }) {
      const res = await dispatch('d2admin/db/get', {
        dbName: 'sys',
        path: 'settings.init',
        defaultValue: {},
        user: true
      }, { root: true })
      // store 赋值
      state.siteName = res.site_name
      state.siteLogo = res.site_logo
      state.loginBackground = res.login_background
      state.loginBanner = res.login_banner
      state.copyright = res.copyright
      state.keepRecord = res.keep_record
    }
  },
  mutations: {
    /**
     * @description 获取配置
     * @param {Object} state state
     * @param {String} key active
     * @param {Object} value active
     */
    async get (state, key, value) {
      return state[key]
    }
  }
}
