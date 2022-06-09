/**
 * 对请求参数进行过滤
 * that=>this
 * array:其他字段数组
 */
const filterParams = function (that, array) {
  const arr = that.crud.columns
  const columnKeys = arr.map(item => {
    return item.key
  })
  const newArray = [...columnKeys, array, 'id']
  return '{' + newArray.toString() + '}'
}

export default filterParams
