import { request } from '@/api/service'
import util from '@/libs/util'
const uploadUrl = process.env.VUE_APP_API + '/api/system/img/'
export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%'
    },
    viewOptions: {
      componentType: 'row'
    },
    formOptions: {
      defaultSpan: 12 // 默认的表单 span
    },
    columns: [
      {
        title: '编码',
        key: 'id',
        width: 90,
        form: {
          disabled: true
        }
      },
      {
        title: '单选本地',
        key: 'select1',
        sortable: true,
        search: {
          disabled: true
        },
        type: 'table-selector',
        dict: {
          url: '/api/system/user/',
          value: 'id', // 数据字典中value字段的属性名
          label: 'name', // 数据字典中label字段的属性名
          getData: (url, dict, { form, component }) => {
            return request({ url: url, params: { page: 1, limit: 1 } }).then(ret => {
              component._elProps.page = ret.data.page
              component._elProps.limit = ret.data.limit
              component._elProps.total = ret.data.total

              return ret.data.data
            })
          }
        },
        form: {
          component: {
            span: 12,
            props: { multiple: true },
            elProps: {
              pagination: true,
              columns: [
                {
                  field: 'name',
                  title: '名称'
                },
                {
                  field: 'username',
                  title: '账号'
                },
                {
                  field: 'role',
                  title: '角色Id'
                },
                {
                  field: 'dept',
                  title: '部门Id'
                }

              ]
            }
          }
        }
      },
      {
        title: '头像',
        key: 'image',
        // type: 'image-uploader',
        type: 'avatar-uploader',
        width: 150,
        align: 'left',
        form: {
          component: {
            props: {
              uploader: {
                action: uploadUrl,
                name: 'file',
                headers: {
                  Authorization: 'JWT ' + util.cookies.get('token')
                },
                type: 'form',
                successHandle (ret, option) {
                  if (ret.data == null || ret.data === '') {
                    throw new Error('上传失败')
                  }
                  return { url: ret.data.data.url, key: option.data.key }
                }
              },
              elProps: { // 与el-uploader 配置一致
                multiple: false,
                limit: 5 // 限制5个文件
              },
              sizeLimit: 50 * 1024 // 不能超过限制
            },
            span: 24
          },
          helper: '限制文件大小不能超过50k'
        },
        valueResolve (row, col) {
          const value = row[col.key]
          if (value != null && value instanceof Array) {
            if (value.length >= 0) {
              row[col.key] = value[0]
            } else {
              row[col.key] = null
            }
          }
        },
        component: {
          props: {
            buildUrl (value, item) {
              if (value && value.indexOf('http') !== 0) {
                return '/api/upload/form/download?key=' + value
              }
              return value
            }
          }
        }
      },
      {
        title: '图片',
        key: 'files',
        type: 'image-uploader',
        width: 150,
        align: 'left',
        form: {
          component: {
            props: {
              uploader: {
                action: uploadUrl,
                name: 'file',
                headers: {
                  Authorization: 'JWT ' + util.cookies.get('token')
                },
                type: 'form',
                successHandle (ret, option) {
                  if (ret.data == null || ret.data === '') {
                    throw new Error('上传失败')
                  }
                  return { url: ret.data.data.url, key: option.data.key }
                }
              },
              elProps: { // 与el-uploader 配置一致
                multiple: false,
                limit: 5 // 限制5个文件
              },
              sizeLimit: 50 * 1024 // 不能超过限制
            },
            span: 24
          },
          helper: '限制文件大小不能超过50k'
        },
        valueResolve (row, col) {
          const value = row[col.key]
          if (value != null && value instanceof Array) {
            if (value.length >= 0) {
              row[col.key] = value[0]
            } else {
              row[col.key] = null
            }
          }
        },
        component: {
          props: {
            buildUrl (value, item) {
              if (value && value.indexOf('http') !== 0) {
                return '/api/upload/form/download?key=' + value
              }
              return value
            }
          }
        }
      },
      {
        title: '多选,本地,自动染色',
        key: 'select2',
        sortable: true,
        width: 180,
        search: {
          disabled: false,
          title: '多选'
        },
        type: 'select',
        form: {
          title: '多选本地',
          component: {
            props: {
              filterable: true,
              multiple: true,
              clearable: true
            }
          }
        },
        dict: {
          data: [{ value: 'sz', label: '深圳' }, { value: 'gz', label: '广州' }, { value: 'wh', label: '武汉' }, { value: 'sh', label: '上海' }]
        },
        component: { props: { color: 'auto' } } // 自动染色
      }
    ]
  }
}
