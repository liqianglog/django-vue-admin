import util from '@/libs/util.js'

export default {
  'image-uploader': {
    form: { component: { name: 'd2p-file-uploader', props: { elProps: { listType: 'picture-card', accept: '.png,.jpeg,.jpg,.ico,.bmp,.gif' } } } },
    component: { name: 'd2p-images-format' },
    view: {
      component: { props: { height: 100, width: 100 } }
    },
    align: 'center',
    // 提交时,处理数据
    valueResolve (row, col) {
      const value = row[col.key]
      if (value != null) {
        if (value.length >= 0) {
          if (value instanceof Array) {
            // 剔除前缀
            row[col.key] = value.map(str => str.replace(util.baseURL(), '')).toString()
          } else {
            // 剔除前缀
            row[col.key] = value.replace(util.baseURL(), '')
          }
        } else {
          row[col.key] = null
        }
      }
    },
    // 接收时,处理数据
    valueBuilder (row, col) {
      const value = row[col.key]
      if (value != null && value) {
        row[col.key] = value.split(',')
        // 进行组装地址，纠正地址
        row[col.key].map((val, index) => {
          if (val.startsWith('/api')) {
            row[col.key][index] = val
          } else if (val.startsWith('/')) {
            row[col.key][index] = util.baseURL() + val.slice(1)
          } else {
            row[col.key][index] = !val.startsWith('http') ? util.baseURL() + val : val
          }
        })
      }
    }
  },
  'avatar-uploader': {
    form: { component: { name: 'd2p-file-uploader', props: { elProps: { limit: 1, listType: 'avatar', accept: '.png,.jpeg,.jpg,.ico,.bmp,.gif', showFileList: false } } } },
    component: { name: 'd2p-images-format' },
    view: {
      component: { props: { height: 100, width: 100 } }
    },
    align: 'center',
    // 提交时,处理数据
    valueResolve (row, col) {
      const value = row[col.key]
      if (value != null) {
        if (value.length >= 0) {
          if (value instanceof Array) {
            // 剔除前缀
            row[col.key] = value.map(str => str.replace(util.baseURL(), '')).toString()
          } else {
            // 剔除前缀
            row[col.key] = value.replace(util.baseURL(), '')
          }
        } else {
          row[col.key] = null
        }
      }
    },
    // 接收时,处理数据
    valueBuilder (row, col) {
      const value = row[col.key]
      if (value != null && value) {
        row[col.key] = value.split(',')
        // 进行组装地址，纠正地址
        row[col.key].map((val, index) => {
          if (val.startsWith('/api')) {
            row[col.key][index] = val
          } else if (val.startsWith('/')) {
            row[col.key][index] = util.baseURL() + val.slice(1)
          } else {
            row[col.key][index] = !val.startsWith('http') ? util.baseURL() + val : val
          }
        })
      }
    }
  },
  'video-uploader': {
    form: { component: { name: 'd2p-file-uploader', props: { elProps: { limit: 1, listType: 'video', accept: '.avi,.wmv,.mpg,.mpeg,.mov,.rm,.ram,.swf,.flv,.mp4,.mp3,.wma,.avi,.rm,.rmvb,.flv,.mpg,.mkv', showFileList: false } } } },
    component: { name: 'd2p-images-format' },
    view: {
      component: { props: { height: 100, width: 100 } }
    },
    align: 'center',
    // 提交时,处理数据
    valueResolve (row, col) {
      const value = row[col.key]
      if (value != null) {
        if (value.length >= 0) {
          if (value instanceof Array) {
            // 剔除前缀
            row[col.key] = value.map(str => str.replace(util.baseURL(), '')).toString()
          } else {
            // 剔除前缀
            row[col.key] = value.replace(util.baseURL(), '')
          }
        } else {
          row[col.key] = null
        }
      }
    },
    // 接收时,处理数据
    valueBuilder (row, col) {
      const value = row[col.key]
      if (value != null && value) {
        row[col.key] = value.split(',')
        // 进行组装地址，纠正地址
        row[col.key].map((val, index) => {
          if (val.startsWith('/api')) {
            row[col.key][index] = val
          } else if (val.startsWith('/')) {
            row[col.key][index] = util.baseURL() + val.slice(1)
          } else {
            row[col.key][index] = !val.startsWith('http') ? util.baseURL() + val : val
          }
        })
      }
    }
  },
  'file-uploader': {
    form: { component: { name: 'd2p-file-uploader', props: { elProps: { listType: 'text' } } } },
    component: { name: 'd2p-files-format' },
    // 提交时,处理数据
    valueResolve (row, col) {
      const value = row[col.key]
      if (value != null) {
        if (value.length >= 0) {
          if (value instanceof Array) {
            // 剔除前缀
            row[col.key] = value.map(str => str.replace(util.baseURL(), '')).toString()
          } else {
            // 剔除前缀
            row[col.key] = value.replace(util.baseURL(), '')
          }
        } else {
          row[col.key] = null
        }
      }
    },
    // 接收时,处理数据
    valueBuilder (row, col) {
      const value = row[col.key]
      if (value != null && value) {
        row[col.key] = value.split(',')
        // 进行组装地址，纠正地址
        row[col.key].map((val, index) => {
          if (val.startsWith('/api')) {
            row[col.key][index] = val
          } else if (val.startsWith('/')) {
            row[col.key][index] = util.baseURL() + val.slice(1)
          } else {
            row[col.key][index] = !val.startsWith('http') ? util.baseURL() + val : val
          }
        })
      }
    }
  },
  'avatar-cropper': {
    form: { component: { name: 'd2p-cropper-uploader', props: { accept: '.png,.jpeg,.jpg,.ico,.bmp,.gif', cropper: { viewMode: 1 } } } },
    component: { name: 'd2p-images-format' },
    align: 'center',
    view: {
      component: { props: { height: 100, width: 100 } }
    },
    // 提交时,处理数据
    valueResolve (row, col) {
      const value = row[col.key]
      if (value != null) {
        if (value.length >= 0) {
          if (value instanceof Array) {
            // 剔除前缀
            row[col.key] = value.map(str => str.replace(util.baseURL(), '')).toString()
          } else {
            // 剔除前缀
            row[col.key] = value.replace(util.baseURL(), '')
          }
        } else {
          row[col.key] = null
        }
      }
    },
    // 接收时,处理数据
    valueBuilder (row, col) {
      const value = row[col.key]
      if (value != null && value) {
        row[col.key] = value.split(',')
        // 进行组装地址，纠正地址
        row[col.key].map((val, index) => {
          if (val.startsWith('/api')) {
            row[col.key][index] = val
          } else if (val.startsWith('/')) {
            row[col.key][index] = util.baseURL() + val.slice(1)
          } else {
            row[col.key][index] = !val.startsWith('http') ? util.baseURL() + val : val
          }
        })
      }
    }
  },
  'tree-selector': {
    form: { component: { name: 'd2p-tree-selector', props: { } } },
    component: { name: 'values-format', props: {} }
  },
  'input-required': {
    form: {
      component: {
        props: { },
        clearable: true,
        placeholder: '请输入'
      },
      rules: [{ required: true, message: '请输入' }],
      itemProps: {
        class: { yxtInput: true }
      }
    }
  },
  input: {
    form: {
      component: {
        props: { },
        clearable: true,
        placeholder: '请输入'
      },
      itemProps: {
        class: { yxtInput: true }
      }
    }
  },
  'editor-ueditor': {
    form: {
      component: {
        name: 'd2p-ueditor',
        span: 24,
        props: {
          config: {
            serverUrl: util.baseURL() + 'api/system/file/ueditor/',
            headers: { Authorization: 'JWT ' + util.cookies.get('token') },
            imageUrlPrefix: util.baseFileURL(),
            // 涂鸦图片上传
            scrawlUrlPrefix: util.baseFileURL(),
            // 截图工具上传
            snapscreenUrlPrefix: util.baseFileURL(),
            // 抓取远程图片路径前缀
            catcherUrlPrefix: util.baseFileURL(),
            // 视频访问路径前缀
            videoUrlPrefix: util.baseFileURL(),
            // 文件访问路径前缀
            fileUrlPrefix: util.baseFileURL(),
            // 列出指定目录下的图片
            imageManagerUrlPrefix: util.baseFileURL(),
            // 列出指定目录下的文件
            fileManagerUrlPrefix: util.baseFileURL()
            // 传入ueditor的配置
            // 文档参考： http://fex.baidu.com/ueditor/#start-config
          }
        }
      }
    }
  }
}
