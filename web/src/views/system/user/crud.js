import { request } from '@/api/service'
import { BUTTON_STATUS_BOOL, USER_TYPE } from '@/config/button'
import { urlPrefix as deptPrefix } from '../dept/api'

export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      tableType: 'vxe-table',
      rowKey: true // 必须设置，true or false
    },
    rowHandle: {
      width: 320,
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
      },
      custom: [
        {
          show () {
            return vm.hasPermissions('ResetPassword')
          },
          disabled () {
            return !vm.hasPermissions('ResetPassword')
          },
          text: '重置密码',
          type: 'warning',
          size: 'small',
          emit: 'resetPassword'
        }
      ]
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
      width: 60
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
        minWidth: 100,
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
              return (< el-alert title="密码默认为:admin123456" type="warning"/>
              )
            }
          }
        }
      },
      {
        title: '姓名',
        key: 'name',
        minWidth: 90,
        search: {
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
        key: 'dept',
        search: {
          disabled: true
        },
        minWidth: 140,
        type: 'table-selector',
        dict: {
          cache: false,
          url: deptPrefix,
          value: 'id', // 数据字典中value字段的属性名
          label: 'name', // 数据字典中label字段的属性名
          getData: (url, dict, { form, component }) => {
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
            pagination: true,
            props: { multiple: false },
            elProps: {
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
      },
      {
        title: '手机号码',
        key: 'mobile',
        search: {
          disabled: true
        },
        minWidth: 110,
        type: 'input',
        form: {
          rules: [
            { max: 20, message: '请输入正确的手机号码', trigger: 'blur' },
            { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码' }
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
        minWidth: 160,
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
        type: 'radio',
        width: 70,
        dict: {
          data: [{ label: '男', value: 1 }, { label: '女', value: 0 }]
        },
        form: {
          value: 1,
          component: {
            span: 12
          }
        },
        component: { props: { color: 'auto' } } // 自动染色
      }, {
        title: '用户类型',
        key: 'user_type',
        search: {
          value: 0,
          disabled: false
        },
        width: 140,
        type: 'select',
        dict: {
          data: USER_TYPE
        },
        form: {
          show: false,
          value: 0,
          component: {
            span: 12
          }
        }
      }, {
        title: '状态',
        key: 'is_active',
        search: {
          disabled: false
        },
        width: 70,
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
        type: 'avatar-cropper',
        width: 60,
        align: 'left',
        form: {
          component: {
            props: {
              elProps: { // 与el-uploader 配置一致
                multiple: false,
                limit: 1 // 限制5个文件
              },
              sizeLimit: 500 * 1024 // 不能超过限制
            },
            span: 24
          },
          helper: '限制文件大小不能超过500k'
        }
      },
      {
        title: '角色',
        key: 'role',
        search: {
          disabled: true
        },
        minWidth: 130,
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
            pagination: true,
            props: { multiple: true },
            elProps: {
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
    ].concat(vm.commonEndColumns({
      create_datetime: { showTable: false },
      update_datetime: { showTable: false }
    }))
  }
}
