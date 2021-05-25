const modelSelect = {
  namespaced: true,
  state: {
    modelSelectMap: {},
  },
  mutations: {
    setModelSelectMap(state, modelSelectMap) {
      state.modelSelectMap = {...state.modelSelectMap, ...modelSelectMap}
    },
  },
  actions: {
    // 从后台获取需要 select 选择数据
    // modelName : 模型 name
    // labelName : 后端接口返回时，配置下拉选择时显示的名字字段，如：name/title/nickName
    // listApi : 查询列表的api
    async getModelSelect({commit, state}, paramsMap) {
      let modelName = paramsMap["modelName"]
      let labelName = paramsMap["labelName"]
      let listApi = paramsMap["listApi"]
      let params = paramsMap["params"]
      if (state.modelSelectMap[modelName]) {
        return state.modelSelectMap[modelName]
      } else {
        const res = await listApi({pageNum: "all", ...params})
        if (res.code === 200) {
          const modelSelectMap = {}
          const dict = []
          res.data && res.data.map(item => {
            dict.push({
              label: item[labelName],
              value: item.id,
              id: item.id,
              parentId: item.parentId
            })
          })
          modelSelectMap[modelName] = dict
          commit("setModelSelectMap", modelSelectMap)
          return state.modelSelectMap[modelName]
        }
      }
    }
  },
  getters: {
    getModelSelect(state) {
      return state.modelSelectMap
    }
  }
}
export default modelSelect
