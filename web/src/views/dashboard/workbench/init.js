const log = [
  {
    i: 'usersTotal0',
    x: 0,
    y: 0,
    w: 12,
    h: 12,
    config: {
      color: {
        label: '背景颜色',
        type: 'color',
        value: 'rgba(255, 255, 255, 1)',
        placeholder: '颜色为空则随机变换颜色'
      },
      fontColor: {
        label: '字体颜色',
        type: 'color',
        value: null,
        placeholder: '请选择字体颜色'
      }
    },
    isResizable: true,
    element: 'usersTotal',
    moved: false
  },
  {
    i: 'loginTotal1',
    x: 12,
    y: 0,
    w: 12,
    h: 12,
    config: {
      color: {
        label: '背景颜色',
        type: 'color',
        value: 'rgba(255, 255, 255, 1)',
        placeholder: '颜色为空则随机变换颜色'
      },
      fontColor: {
        label: '字体颜色',
        type: 'color',
        value: null,
        placeholder: '请选择字体颜色'
      }
    },
    isResizable: true,
    element: 'loginTotal',
    moved: false
  },
  {
    i: 'attachmentTotal2',
    x: 24,
    y: 0,
    w: 12,
    h: 12,
    config: {
      color: {
        label: '背景颜色',
        type: 'color',
        value: 'rgba(255, 255, 255, 1)',
        placeholder: '颜色为空则随机变换颜色'
      },
      fontColor: {
        label: '字体颜色',
        type: 'color',
        value: null,
        placeholder: '请选择字体颜色'
      }
    },
    isResizable: true,
    element: 'attachmentTotal',
    moved: false
  },
  {
    i: 'databaseTotal3',
    x: 36,
    y: 0,
    w: 12,
    h: 12,
    config: {
      color: {
        label: '背景颜色',
        type: 'color',
        value: 'rgba(255, 255, 255, 1)',
        placeholder: '颜色为空则随机变换颜色'
      },
      fontColor: {
        label: '字体颜色',
        type: 'color',
        value: null,
        placeholder: '请选择字体颜色'
      }
    },
    isResizable: true,
    element: 'databaseTotal',
    moved: false
  },
  {
    i: 'userLogin6',
    x: 14,
    y: 12,
    w: 17,
    h: 24,
    config: {},
    isResizable: true,
    element: 'userLogin',
    moved: false
  },
  {
    i: 'registeredUser7',
    x: 31,
    y: 12,
    w: 17,
    h: 24,
    config: {},
    isResizable: true,
    element: 'registeredUser',
    moved: false
  },
  {
    i: 'dashboardImg8',
    x: 14,
    y: 58,
    w: 16,
    h: 14,
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
  },
  {
    i: 'dashboardImg9',
    x: 0,
    y: 58,
    w: 14,
    h: 14,
    config: {
      src: {
        label: '图片地址',
        type: 'input',
        value: '/image/card/tencent.jpg',
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
    i: 'dashboardImg10',
    x: 30,
    y: 58,
    w: 18,
    h: 14,
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
    i: 'usersActive11',
    x: 0,
    y: 12,
    w: 14,
    h: 24,
    config: {
      color: {
        label: '背景颜色',
        type: 'color',
        value: '',
        placeholder: '颜色为空则随机变换颜色'
      },
      fontColor: {
        label: '字体颜色',
        type: 'color',
        value: null,
        placeholder: '请选择字体颜色'
      }
    },
    isResizable: true,
    element: 'usersActive',
    moved: false
  },
  {
    i: 'ver11',
    x: 35,
    y: 36,
    w: 13,
    h: 22,
    config: {
      showHeader: {
        label: '显示头部信息',
        type: 'boot',
        value: true,
        placeholder: '颜色为空则随机变换颜色'
      },
      color: {
        label: '背景颜色',
        type: 'color',
        value: 'rgba(255, 255, 255, 1)',
        placeholder: '颜色为空则随机变换颜色'
      },
      fontColor: {
        label: '字体颜色',
        type: 'color',
        value: null,
        placeholder: '请选择字体颜色'
      }
    },
    isResizable: true,
    element: 'ver',
    moved: false
  },
  {
    i: 'loginRegion12',
    x: 0,
    y: 36,
    w: 35,
    h: 22,
    config: {},
    isResizable: true,
    element: 'loginRegion',
    moved: false
  }
]
export default log
