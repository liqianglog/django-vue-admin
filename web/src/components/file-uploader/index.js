import D2pImagesFormat from './lib/images-format'
import D2pFilesFormat from './lib/files-format'
import 'cropperjs/dist/cropper.css'
import D2pUploader from 'd2p-extends/src/uploader'

function install (Vue, options) {
  Vue.component('d2p-file-uploader', () => import('./lib/file-uploader'))
  Vue.component('d2p-images-format', D2pImagesFormat)
  Vue.component('d2p-cropper-uploader', () => import('./lib/cropper-uploader'))
  Vue.component('d2p-cropper', () => import('./lib/cropper'))
  Vue.component('d2p-files-format', D2pFilesFormat)

  if (options != null) {
    Vue.use(D2pUploader, options)
  }
}

const createAllUploadedValidator = (getFormComponentRef) => {
  return (rule, value, callback) => {
    const ref = getFormComponentRef(rule.fullField)
    if (ref && ref.isHasUploadingItem()) {
      callback(new Error('还有未上传完成的文件'))
      return
    }
    callback()
  }
}

export default {
  install,
  createAllUploadedValidator
}
