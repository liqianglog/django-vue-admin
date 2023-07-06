export default {
  // 字段类型配置，注册之后即可在crud.js中使用了
  'foreign-key-crud-form': {
    // 行组件配置
    form: { component: { name: 'foreign-key-crud-form', props: { color: 'danger' } } },
    component: {
      name: 'values-popover',
      props: {
        elProps: {
          type: 'list',
          rowKey: 'name'
        }
      }
    },
    // 行展示时居中
    align: 'center'
    // 您还可以写更多默认配置
  }
}
