import { request } from '@/api/service'
import { BUTTON_STATUS_BOOL } from '@/config/button'
import { urlPrefix as deptPrefix } from '../dept/api'
import util from '@/libs/util'
const uploadUrl = util.baseURL() + 'api/system/img/'
export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%'
    },
    rowHandle: {
      width: 140,
      fixed: 'right',
      view: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      edit: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Delete')
        }
      }
    },
    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 12 // 默认的表单 span
    },
    indexRow: { // 或者直接传true,不显示title，不居中
      title: '序号',
      align: 'center',
      width: 80
    },
    columns: [
      {
        title: '关键词',
        key: 'search',
        show: false,
        disabled: true,
        search: {
          disabled: false
        },
        form: {
          disabled: true,
          component: {
            placeholder: '请输入关键词'
          }
        },
        view: {
          disabled: true
        }
      },
      {
        title: 'ID',
        key: 'id',
        width: 90,
        disabled: true,
        form: {
          disabled: true
        }
      },
      {
        title: '账号',
        key: 'username',
        search: {
          disabled: false
        },
        width: 160,
        type: 'input',
        form: {
          rules: [ // 表单校验规则
            { required: true, message: '账号必填项' }
          ],
          component: {
            placeholder: '请输入账号'
          },
          itemProps: {
            class: { yxtInput: true }
          },
          helper: {
            render (h) {
              return (< el-alert title="密码默认为:admin123456" type="warning" />
              )
            }
          }
        }
      },
      {
        title: '姓名',
        key: 'name',
        search: {
          key: 'name__icontains',
          disabled: false
        },
        type: 'input',
        form: {
          rules: [ // 表单校验规则
            { required: true, message: '姓名必填项' }
          ],
          component: {
            span: 12,
            placeholder: '请输入姓名'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '部门',
        width: 160,
        key: 'dept',
        search: {
          disabled: true
        },
        type: 'table-selector',
        dict: {
          cache: false,
          url: deptPrefix,
          value: 'id', // 数据字典中value字段的属性名
          label: 'name', // 数据字典中label字段的属性名
          getData: (url, dict, { _, component }) => {
            return request({ url: url, params: { page: 1, limit: 10, status: 1 } }).then(ret => {
              component._elProps.page = ret.data.page
              component._elProps.limit = ret.data.limit
              component._elProps.total = ret.data.total
              return ret.data.data
            })
          }
        },
        form: {
          rules: [ // 表单校验规则
            { required: true, message: '必填项' }
          ],
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            span: 12,
            props: { multiple: false },
            elProps: {
              pagination: true,
              columns: [
                {
                  field: 'name',
                  title: '部门名称'
                },
                {
                  field: 'status_label',
                  title: '状态'
                },
                {
                  field: 'parent_name',
                  title: '父级部门'
                }
              ]
            }
          }
        }
      }, {
        title: '手机号码',
        key: 'mobile',
        width: 120,
        search: {
          disabled: true
        },
        type: 'input',
        form: {
          rules: [
            { max: 20, message: '请输入正确的手机号码', trigger: 'blur' },
            { pattern: /^1[3|4|5|7|8]\d{9}$/, message: '请输入正确的手机号码' }
          ],
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            placeholder: '请输入手机号码'
          }
        }
      }, {
        title: '邮箱',
        key: 'email',
        width: 120,
        form: {
          rules: [
            { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
          ],
          component: {
            placeholder: '请输入邮箱'
          }
        }
      },
      {
        title: '性别',
        key: 'gender',
        type: 'select',
        dict: {
          data: [{ label: '男', value: 1 }, { label: '女', value: 0 }]
        },
        form: {
          value: 1,
          rules: [
            { required: true, message: '性别必填项' }
          ],
          component: {
            span: 12
          },
          itemProps: {
            class: { yxtInput: true }
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      },
      {
        title: '用户类型',
        key: 'user_type',
        type: 'select',
        width: 120,
        search: {
          key: 'user_type',
          value: 0,
          disabled: false
        },
        dict: {
          data: [{ label: '前台用户', value: 1 }, { label: '后台用户', value: 0 }]
        },
        form: {
          disabled: true
        },
        component: { props: { color: 'auto' } } // 自动染色
      },
      {
        title: '状态',
        key: 'is_active',
        search: {
          disabled: false
        },
        width: 90,
        type: 'radio',
        dict: {
          data: BUTTON_STATUS_BOOL
        },
        form: {
          value: true,
          component: {
            span: 12
          }
        }
      },
      {
        title: '头像',
        key: 'avatar',
        type: 'avatar-uploader',
        width: 80,
        align: 'left',
        form: {
          component: {
            props: {
              uploader: {
                action: uploadUrl,
                name: 'url',
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
                multiple: true,
                limit: 5 // 限制5个文件
              },
              sizeLimit: 100 * 1024 // 不能超过限制
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
              console.log(11, value)
              if (value && value.indexOf('http') !== 0) {
                return '/api/upload/form/download?key=' + value
              }
              return value
            }
          }
        }
      },
      {
        title: '角色',
        key: 'role',
        width: 160,
        search: {
          disabled: true
        },
        type: 'table-selector',
        dict: {
          cache: false,
          url: '/api/system/role/',
          value: 'id', // 数据字典中value字段的属性名
          label: 'name', // 数据字典中label字段的属性名
          getData: (url, dict, { form, component }) => {
            return request({ url: url, params: { page: 1, limit: 10 } }).then(ret => {
              component._elProps.page = ret.data.page
              component._elProps.limit = ret.data.limit
              component._elProps.total = ret.data.total
              return ret.data.data
            })
          }
        },
        form: {
          rules: [ // 表单校验规则
            { required: true, message: '必填项' }
          ],
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            span: 12,
            props: { multiple: true },
            elProps: {
              pagination: true,
              columns: [
                {
                  field: 'name',
                  title: '角色名称'
                },
                {
                  field: 'key',
                  title: '权限标识'
                },
                {
                  field: 'status_label',
                  title: '状态'
                }
              ]
            }
          }
        }
      }
    ].concat(vm.commonEndColumns({ update_datetime: { showTable: false } }))
  }
}
