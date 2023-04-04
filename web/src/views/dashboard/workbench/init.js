const log = [
  {
    i: 'dashboardImg1',
    x: 9,
    y: 21,
    w: 8,
    h: 24,
    minW: 1,
    minH: 10,
    maxW: 24,
    maxH: 100,
    config: {
      src: {
        label: '图片地址',
        type: 'input',
        value: '/image/card/tencent.jpg',
        rules: [
          {
            required: true,
            message: '不能为空'
          }
        ]
      },
      url: {
        label: '跳转地址',
        type: 'input',
        value: 'https://cloud.tencent.com/act/cps/redirect?redirect=1060&cps_key=b302a514a6688aa30823fac954464e5d&from=console',
        rules: [
          {
            required: true,
            message: '不能为空'
          }
        ]
      }
    },
    isResizable: true,
    element: 'dashboardImg',
    moved: false
  },
  {
    i: 'dashboardImg2',
    x: 9,
    y: 0,
    w: 15,
    h: 21,
    minW: 1,
    minH: 10,
    maxW: 24,
    maxH: 100,
    config: {
      src: {
        label: '图片地址',
        type: 'input',
        value: 'https://kfm-waiter.oss-cn-zhangjiakou.aliyuncs.com/dvadmin/img/aliyun-02.png',
        placeholder: '请输入图片地址',
        rules: [
          {
            required: true,
            message: '不能为空'
          }
        ]
      },
      url: {
        label: '跳转地址',
        type: 'input',
        placeholder: '请输入跳转地址',
        value: 'https://www.aliyun.com/minisite/goods?userCode=jpef8a71&share_source=copy_link',
        rules: [
          {
            required: true,
            message: '不能为空'
          }
        ]
      }
    },
    isResizable: true,
    element: 'dashboardImg',
    moved: false
  },
  {
    i: 'time3',
    x: 9,
    y: 45,
    w: 8,
    h: 19,
    minW: 4,
    minH: 10,
    maxW: null,
    maxH: 100,
    config: {},
    isResizable: true,
    element: 'time',
    moved: false
  },
  {
    i: 'ver4',
    x: 17,
    y: 45,
    w: 7,
    h: 19,
    minW: 4,
    minH: 10,
    maxW: null,
    maxH: 100,
    config: {},
    isResizable: true,
    element: 'ver',
    moved: false
  },
  {
    i: 'about5',
    x: 0,
    y: 45,
    w: 9,
    h: 19,
    minW: 2,
    minH: 10,
    maxW: null,
    maxH: 100,
    config: {
      color: {
        label: '背景颜色',
        type: 'color',
        value: null,
        placeholder: '颜色为空则随机变换颜色'
      }
    },
    isResizable: true,
    element: 'about',
    moved: false
  },
  {
    i: 'welcome5',
    x: 0,
    y: 0,
    w: 9,
    h: 45,
    minW: 1,
    minH: 45,
    maxW: null,
    maxH: 100,
    config: {},
    isResizable: true,
    element: 'welcome',
    moved: false
  },
  {
    i: 'dashboardImg6',
    x: 17,
    y: 21,
    w: 7,
    h: 24,
    minW: 1,
    minH: 10,
    maxW: 24,
    maxH: 100,
    config: {
      src: {
        label: '图片地址',
        type: 'input',
        value: 'https://kfm-waiter.oss-cn-zhangjiakou.aliyuncs.com/dvadmin/img/chajianshichang.jpg',
        placeholder: '请输入图片地址',
        rules: [
          {
            required: true,
            message: '不能为空'
          }
        ]
      },
      url: {
        label: '跳转地址',
        type: 'input',
        placeholder: '请输入跳转地址',
        value: 'https://bbs.django-vue-admin.com/plugMarket.html',
        rules: [
          {
            required: true,
            message: '不能为空'
          }
        ]
      }
    },
    isResizable: true,
    element: 'dashboardImg',
    moved: false
  }
]
export default log
