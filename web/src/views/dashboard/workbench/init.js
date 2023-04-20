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
        value: 'rgba(70, 183, 146, 1)',
        placeholder: '请选择字体颜色'
      }
    },
    isResizable: true,
    element: 'usersTotal',
    moved: false,
    hpx: 122,
    wpx: 397
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
        value: 'rgba(30, 144, 255, 1)',
        placeholder: '请选择字体颜色'
      }
    },
    isResizable: true,
    element: 'loginTotal',
    moved: false,
    hpx: 122,
    wpx: 397
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
        value: 'rgba(255, 140, 0, 1)',
        placeholder: '请选择字体颜色'
      }
    },
    isResizable: true,
    element: 'attachmentTotal',
    moved: false,
    hpx: 122,
    wpx: 397
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
        value: 'rgba(0, 186, 189, 1)',
        placeholder: '请选择字体颜色'
      }
    },
    isResizable: true,
    element: 'databaseTotal',
    moved: false,
    hpx: 122,
    wpx: 397
  },
  {
    i: 'usersActive5',
    x: 33,
    y: 12,
    w: 15,
    h: 24,
    config: {},
    isResizable: true,
    element: 'usersActive',
    moved: false,
    hpx: 254,
    wpx: 498
  },
  {
    i: 'userLogin6',
    x: 0,
    y: 12,
    w: 16,
    h: 24,
    config: {},
    isResizable: true,
    element: 'userLogin',
    moved: false,
    hpx: 254,
    wpx: 532
  },
  {
    i: 'registeredUser7',
    x: 16,
    y: 12,
    w: 17,
    h: 24,
    config: {},
    isResizable: true,
    element: 'registeredUser',
    moved: false,
    hpx: 254,
    wpx: 566
  },
  {
    i: 'dashboardImg8',
    x: 32,
    y: 36,
    w: 16,
    h: 24,
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
    moved: false,
    hpx: 254,
    wpx: 532
  },
  {
    i: 'dashboardImg9',
    x: 16,
    y: 36,
    w: 16,
    h: 24,
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
    moved: false,
    hpx: 254,
    wpx: 532
  },
  {
    i: 'dashboardImg10',
    x: 16,
    y: 60,
    w: 22,
    h: 15,
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
    moved: false,
    hpx: 155,
    wpx: 736
  },
  {
    i: 'welcome10',
    x: 0,
    y: 36,
    w: 16,
    h: 39,
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
        value: 'rgba(0, 0, 0, 1)',
        placeholder: '请选择字体颜色'
      }
    },
    isResizable: true,
    element: 'welcome',
    moved: false,
    hpx: 419,
    wpx: 532
  },
  {
    i: 'ver11',
    x: 38,
    y: 60,
    w: 10,
    h: 15,
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
        value: 'rgba(30, 144, 255, 1)',
        placeholder: '请选择字体颜色'
      }
    },
    isResizable: true,
    element: 'ver',
    moved: false,
    hpx: 155,
    wpx: 329
  }
]
export default log
