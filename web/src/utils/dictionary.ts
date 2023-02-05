import { toRaw } from 'vue';
import { DictionaryStore } from '/@/stores/dictionary';

/** 
  * @method 获取指定name字典 
  */
export const dictionary = (name: string) => {
  const dict = DictionaryStore()
  const dictionary = toRaw(dict.data)
  return dictionary[name]
}