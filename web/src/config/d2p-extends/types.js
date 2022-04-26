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
            row[col.key] = value.toString()
          } else {
            row[col.key] = value[0]
          }
        } else {
          row[col.key] = null
        }
      }
    },
    // 接收时,处理数据
    valueBuilder (row, col) {
      const value = row[col.key]
      if (value != null) {
        row[col.key] = value.split(',')
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
            row[col.key] = value.toString()
          } else {
            row[col.key] = value[0]
          }
        } else {
          row[col.key] = null
        }
      }
    },
    // 接收时,处理数据
    valueBuilder (row, col) {
      const value = row[col.key]
      if (value != null) {
        row[col.key] = value.split(',')
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
            row[col.key] = value.toString()
          } else {
            row[col.key] = value[0]
          }
        } else {
          row[col.key] = null
        }
      }
    },
    // 接收时,处理数据
    valueBuilder (row, col) {
      const value = row[col.key]
      if (value != null) {
        row[col.key] = value.split(',')
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
    // 接收时,处理数据
    valueBuilder (row, col) {
      const value = row[col.key]
      if (value != null) {
        row[col.key] = value.split(',')
      }
    }
  }
}
