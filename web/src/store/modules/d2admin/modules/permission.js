import { request } from '@/api/service'
const urlPrefix = '/api/system/menu_button/get_btn_permission/'
export default {
  namespaced: true,
  state: {
    // 未读消息
    data: []
  },
  getters: {
    permissionList (state) {
      return state.data
    }
  },
  actions: {
    /**
     * @description 获取数据
     * @param {Object} context
     * @param {String} param message {String} 信息
     * @param {String} param type {String} 类型
     * @param {Object} payload meta {Object} 附带的信息
     */
    async load ({
      state,
      commit
    }) {
      request({
        url: urlPrefix,
        method: 'get',
        params: {}
      }).then(res => {
        const { data } = res
        commit('set', data)
      })
    }
  },
  mutations: {
    /**
     * 设置权限数据
     * @param state
     * @param number
     */
    async set (state, data) {
      state.data = data
    }
  }
}
