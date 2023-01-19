import { BUTTON_WHETHER_BOOL } from '@/config/button'
export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      tableType: 'vxe-table',
      rowKey: true, // 必须设置，true or false
      rowId: 'id',
      height: '100%', // 表格高度100%, 使用toolbar必须设置
      highlightCurrentRow: false

    },
    rowHandle: {
      view: {
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      width: 240,
      edit: {
        thin: true,
        text: '编辑',
        disabled () {
          return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: '删除',
        disabled () {
          return !vm.hasPermissions('Delete')
        }
      }
    },
    indexRow: { // 或者直接传true,不显示title，不居中
      title: '序号',
      align: 'center',
      width: 100
    },

    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 24, // 默认的表单 span
      width: '35%',
      saveRemind: true
    },
    columns: [{
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
          placeholder: '请输入关键词',
          props: {
            clearable: true
          }
        }
      },
      view: { // 查看对话框组件的单独配置
        disabled: true
      }
    },
    {
      title: 'ID',
      key: 'id',
      show: false,
      width: 90,
      form: {
        disabled: true
      }
    },

    {
      title: '域名',
      key: 'domain',
      sortable: true,
      search: {
        disabled: false,
        component: {
          placeholder: '请输入域名',
          props: {
            clearable: true
          }
        }
      },

      type: 'input',
      form: {
        rules: [ // 表单校验规则
          { required: true, message: '域名必填项' },
          { min: 1, max: 253, message: '长度在 1 到 253 个字符', trigger: 'blur' },
          {
            trigger: ['change', 'blur'],
            pattern: /^[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?$/,
            message: '域名的字符串无效'
          }
        ],
        component: {
          placeholder: '请输入域名',
          props: {
            clearable: true
          }
        },
        itemProps: {
          class: { yxtInput: true }
        }
      }
    }, {
      title: '是否为主域',
      key: 'is_primary',
      sortable: true,
      type: 'radio',
      dict: {
        data: BUTTON_WHETHER_BOOL
      },
      search: {
        disabled: false
      },
      form: {
        value: true,
        component: {
        }
      }
    }
    ]
  }
}
