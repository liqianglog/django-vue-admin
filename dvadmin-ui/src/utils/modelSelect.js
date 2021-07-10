import store from "@/store";
//  获取字典方法 使用示例 this.getModelSelect(this.prop, this.label_name, this.listApi).then(res)
//  或者 async函数下 const res = await this.getModelSelect(this.prop, this.label_name, this.listApi)
export const getModelSelect = async(modelName, labelName, listApi, params, reset) => {
  await store.dispatch("modelSelect/getModelSelect", { modelName, labelName, listApi, params, reset });
  return store.getters["modelSelect/getModelSelect"][modelName];
};
