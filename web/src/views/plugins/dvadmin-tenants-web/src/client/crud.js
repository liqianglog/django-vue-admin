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
      fixed: 'right',
      view: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      width: 310,
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
      },
      custom: [{
        text: ' 域名管理',
        type: 'warning',
        size: 'small',
        icon: 'el-icon-link',
        emit: 'selectDomain'
      }]
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
      width: '35%'
    },
    columns: [{
      title: '关键词',
      key: 'search',
      show: false,
      disabled: true,
      search: {
        disabled: true
      },
      form: {
        disabled: true,
        component: {
          props: {
            clearable: true
          },
          placeholder: '请输入关键词'
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
      width: 70,
      form: {
        disabled: true
      }
    },

    {
      title: '租户标识',
      key: 'schema_name',
      sortable: true,
      minWidth: 100,
      search: {
        disabled: false,
        component: {
          props: {
            clearable: true
          }
        }
      },

      type: 'input',
      form: {
        rules: [ // 表单校验规则
          { required: true, message: '租户标识必填项' },
          { min: 1, max: 63, message: '长度在 1 到 63 个字符', trigger: 'blur' },
          { trigger: ['change', 'blur'], pattern: /^[_a-zA-Z0-9]{1,63}$/, message: '名称的字符串无效' }
        ],
        component: {
          placeholder: '请输入租户标识',
          props: {
            clearable: true
          },
          disabled (context) { if (context.mode === 'edit') return true }
        },
        itemProps: {
          class: { yxtInput: true }
        }
      }
    }, {
      title: '租户名称',
      key: 'name',
      sortable: true,
      minWidth: 180,
      search: {
        disabled: false,
        component: {
          props: {
            clearable: true
          }
        }
      },

      type: 'input',
      form: {
        rules: [ // 表单校验规则
          { required: true, message: '租户名称必填项' }
        ],
        component: {
          placeholder: '请输入租户名称',
          props: {
            clearable: true
          }
        },
        itemProps: {
          class: { yxtInput: true }
        }
      }
    },
    {
      title: '生效开始',
      key: 'start_datetime',
      type: 'date',
      sortable: true,
      form: {
        rules: [ // 表单校验规则
          { required: true, message: '开始时间必填项' }
        ],
        component: {
          placeholder: '请选择开始时间',
          props: {
            clearable: true,
            'value-format': 'yyyy-MM-dd'
          }
        },
        itemProps: {
          class: { yxtInput: true }
        }
      }
    }, {
      title: '生效结束',
      key: 'paid_until',
      type: 'date',
      sortable: true,
      form: {
        rules: [ // 表单校验规则
          { required: true, message: '生效结束必填项' }
        ],
        component: {
          placeholder: '请选择生效结束',
          props: {
            clearable: true,
            'value-format': 'yyyy-MM-dd'
          }
        },
        itemProps: {
          class: { yxtInput: true }
        }
      }
    }, {
      title: '是否启用',
      key: 'on_trial',
      type: 'radio',
      width: 75,
      fixed: 'right',
      dict: {
        data: BUTTON_WHETHER_BOOL
      },
      search: {
        disabled: false
      },
      form: {
        value: true,
        rules: [
          { required: true, message: '是否启用不能为空', trigger: 'blur' }
        ],
        component: {
          span: 24,
          placeholder: '请选择是否启用'
        },
        itemProps: {
          class: { yxtInput: true }
        }
      }
    },
    {
      title: '创建人',
      show: false,
      width: 100,
      key: 'modifier_name',
      form: {
        disabled: true
      }
    },
    {
      title: '创建时间',
      key: 'created_on',
      show: false,
      type: 'date',
      sortable: true,
      form: {
        disabled: true
      }
    }
    ]
  }
}
