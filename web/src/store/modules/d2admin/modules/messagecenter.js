import { request } from '@/api/service'
export default {
  namespaced: true,
  state: {
    // 未读消息
    unread: 0
  },
  getters: {
    unread (state) {
      return state.unread
    }
  },
  actions: {
    /**
     * @description 添加一个日志
     * @param {Object} context
     * @param {String} param message {String} 信息
     * @param {String} param type {String} 类型
     * @param {Object} payload meta {Object} 附带的信息
     */
    async setUnread ({
      state,
      commit
    }, number) {
      if (number) {
        commit('set', number)
      } else {
        request({
          url: '/api/system/message_center/get_unread_msg/',
          method: 'get',
          params: {}
        }).then(res => {
          const { data } = res
          commit('set', data.count)
        })
      }
    }
  },
  mutations: {
    /**
     * 设置未读消息
     * @param state
     * @param number
     */
    async set (state, number) {
      state.unread = number
    }
  }
}
