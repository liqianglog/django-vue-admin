import { request } from '@/api/service'

export const urlPrefix = '/api/init/settings/'

// 系统配置
export default {
  namespaced: true,
  state: {
    siteName: '', // 网站名称
    siteLogo: '', // 网站logo地址
    loginBackground: '', // 登录页背景图
    copyright: '', // 版权
    keepRecord: '', // 备案
    helpUrl: '', // 帮助地址
    privacyUrl: '', // 隐私
    clauseUrl: '', // 条款
    captchaState: true // 是否开启验证码
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
      state.copyright = res.copyright
      state.keepRecord = res.keep_record
      state.helpUrl = res.help_url
      state.privacyUrl = res.privacy_url
      state.clauseUrl = res.clause_url
      state.captchaState = res.captcha_state
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
