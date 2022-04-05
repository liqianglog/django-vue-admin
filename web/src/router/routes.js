import layoutHeaderAside from '@/layout/header-aside'

// 由于懒加载页面太多的话会造成webpack热更新太慢，所以开发环境不使用懒加载，只有生产环境使用懒加载
const _import = require('@/libs/util.import.' + process.env.NODE_ENV)

/**
 * 在主框架内显示
 */
const frameIn = [{
  path: '/',
  redirect: { name: 'index' },
  component: layoutHeaderAside,
  children: [
    // 控制台
    {
      path: 'index',
      name: 'index',
      meta: {
        auth: true
      },
      component: _import('dashboard/workbench/index')
    },
    {
      path: 'userInfo',
      name: 'userInfo',
      meta: {
        title: '个人信息',
        auth: true
      },
      component: () => import('@/layout/header-aside/components/header-user/userinfo')
    },
    // 演示页面
    {
      path: 'page1',
      name: 'page1',
      meta: {
        title: '页面 1',
        auth: true
      },
      component: _import('demo/page1')
    },
    {
      path: 'page2',
      name: 'page2',
      meta: {
        title: '页面 2',
        auth: true
      },
      component: _import('demo/page2')
    },
    {
      path: 'page3',
      name: 'page3',
      meta: {
        title: '页面 3',
        auth: true
      },
      component: _import('demo/page3')
    },
    // dashboard 工作台
    {
      path: 'workbench',
      name: 'workbench',
      meta: {
        title: '工作台',
        auth: true
      },
      component: _import('dashboard/workbench')
    },
    // // 系统 菜单
    // {
    //   path: 'menu',
    //   name: 'menu',
    //   meta: {
    //     title: '菜单',
    //     auth: true
    //   },
    //   component: _import('system/menu')
    // },
    // // 系统 用户
    // {
    //   path: 'user',
    //   name: 'user',
    //   meta: {
    //     title: '用户',
    //     auth: true
    //   },
    //   component: _import('system/user')
    // },
    // // 系统 按钮配置
    {
      path: 'button',
      name: 'button',
      meta: {
        title: '按钮',
        auth: true
      },
      component: _import('system/button')
    },
    // // 系统 菜单权限
    {
      path: 'menuButton/:id',
      name: 'menuButton',
      meta: {
        title: '菜单按钮',
        auth: true
      },
      component: _import('system/menuButton')
    },
    // // 系统 角色管理
    // {
    //   path: 'role',
    //   name: 'role',
    //   meta: {
    //     title: '角色',
    //     auth: true
    //   },
    //   component: _import('system/role')
    // },
    // // 系统 角色权限
    // {
    //   path: 'rolePermission',
    //   name: 'rolePermission',
    //   meta: {
    //     title: '权限管理',
    //     auth: true
    //   },
    //   component: _import('system/rolePermission')
    // },

    // // 系统 角色管理
    // {
    //   path: 'dept',
    //   name: 'dept',
    //   meta: {
    //     title: '部门',
    //     auth: true
    //   },
    //   component: _import('system/dept')
    // },
    // // 系统 操作日志
    // {
    //   path: 'operationLog',
    //   name: 'operationLog',
    //   meta: {
    //     title: '操作日志',
    //     auth: true
    //   },
    //   component: _import('system/log/operationLog')
    // },
    // 系统 前端日志
    {
      path: 'frontendLog',
      name: 'frontendLog',
      meta: {
        title: '前端日志',
        auth: true
      },
      component: _import('system/log/frontendLog')
    },
    // 刷新页面 必须保留
    {
      path: 'refresh',
      name: 'refresh',
      hidden: true,
      component: _import('system/function/refresh')
    },
    // 页面重定向 必须保留
    {
      path: 'redirect/:route*',
      name: 'redirect',
      hidden: true,
      component: _import('system/function/redirect')
    }
  ]
}]

/**
 * 在主框架之外显示
 */
const frameOut = [
  // 登录
  {
    path: '/login',
    name: 'login',
    component: _import('system/login')
  }
]

/**
 * 错误页面
 */
const errorPage = [{
  path: '*',
  name: '404',
  component: _import('system/error/404')
}]

// 导出需要显示菜单的
export const frameInRoutes = frameIn

// 重新组织后导出
export default [
  ...frameIn,
  ...frameOut,
  ...errorPage
]
