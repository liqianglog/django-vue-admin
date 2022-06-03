// 导入各个组件
// 把组件保存到一个数组中
import { registerMicroApps, start } from 'qiankun'
const components = [
]

// 定义 install 方法
const install = function (Vue) {
  if (install.installed) return
  install.installed = true
  // 遍历组件列表并注册全局组件
  components.map(component => {
    Vue.component(component.name, component) // component.name 此处使用到组件vue文件中的 name 属性
  })
}

if (typeof window !== 'undefined' && window.Vue) {
  install(window.Vue)
}
if (!window.qiankunActiveRule) {
  window.qiankunActiveRule = []
}
window.qiankunActiveRule.push('drag-h5')
registerMicroApps([
  {
    name: 'drag-h5', // 应用的名字
    entry: '//localhost:8082', // 默认会加载这个html 解析里面的js 动态的执行 （子应用必须支持跨域）fetch
    container: '#qiankun', // 容器id
    activeRule: '/#/drag-h5' // 根据路由 激活的路径
  }
])
start({ prefetch: 'all' })
export default {
  // 导出的对象必须具备一个 install 方法
  install,
  // 组件列表
  ...components
}
