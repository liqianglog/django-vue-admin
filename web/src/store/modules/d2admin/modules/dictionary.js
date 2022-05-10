import { request } from '@/api/service'

export const urlPrefix = '/api/system/dictionary/'

// 系统配置
export default {
  namespaced: true,
  state: {
    data: {} // 字典值集合
  },
  actions: {
    /**
     * @description 本地加载配置
     * @param {Object} context
     * @param {String} key
     */
    async load ({ state, dispatch, commit }, key = 'all') {
      const query = { dictionary_key: key }
      request({
        url: urlPrefix,
        params: query,
        method: 'get'
      }).then(async res => {
        // store 赋值
        var newData = {}
        if (key === 'all') {
          res.data.data.map(data => {
            data.children.map((children, index) => {
              console.log(children.type)
              switch (children.type) {
                case 1:
                  children.value = Number(children.value)
                  break
                case 6:
                  children.value = children.value === 'true'
                  break
              }
            })
            newData[data.value] = data.children
          })
          console.log(11, newData)
          state.data = newData
        } else {
          state.data = res.data.data[key]
        }
      })
    }
    /**
     * @description 获取配置
     * @param {Object} state state
     * @param {Object} dispatch dispatch
     * @param {String} key 字典值
     * @param {String} isCache 是否缓存
     */
  },
  mutations: {
    /**
     * @description 设置配置
     * @param {Object} state state
     * @param {Boolean} key active
     * @param {Boolean} value active
     */
    async set (state, key, value) {
      state.data[key] = value
    },
    /**
     * @description 获取配置
     * @param {Object} state state
     * @param {Boolean} key active
     */
    async get (state, key) {
      console.log(1212, state.data[key])
      return state.data[key]
    }
  }
}
