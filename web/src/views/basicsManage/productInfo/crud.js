import { BUTTON_STATUS_NUMBER } from '@/config/button'
import util from '@/libs/util'

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
      width: 140,
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
      componentType: 'row'
    },
    formOptions: {
      defaultSpan: 24 // 默认的表单 span
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
          disabled: false,
          component: {
            props: {
              clearable: true
            }
          }
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
        view: {
          disabled: true
        }
      }, {
        title: 'ID',
        key: 'id',
        show: false,
        form: {
          disabled: true
        }
      },
      {
        title: '编号',
        key: 'no',
        width: 120,
        search: {
          disabled: true,
          component: {
            props: {
              clearable: true
            }
          }
        },
        type: 'input',
        form: {
          rules: [
            { required: true, message: '编号不能为空', trigger: 'blur' }
          ],
          component: {
            placeholder: '请输入编号'
          },
          itemProps: {
            class: { yxtInput: true }
          },
          valueChange (key, value, form, { getColumn, mode, component, immediate, getComponent }) {
            if (mode === 'add' && !form.no) {
              form.no = util.autoShortCreateCode()
            }
          },
          valueChangeImmediate: true
        }
      }, {
        title: '产品名称',
        key: 'name',
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
          rules: [
            { required: true, message: '产品名称不能为空', trigger: 'blur' }
          ],
          component: {
            placeholder: '请输入产品名称'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '产品图片',
        key: 'img',
        type: 'avatar-uploader',
        minWidth: 100,
        search: {
          disabled: true
        },
        form: {
          component: {
            props: {
              clearable: true
            },
            placeholder: '请选择提交图片'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '关联客户',
        key: 'customer_info',
        type: 'selector-table',
        minWidth: 120,
        dict: {
          cache: false, // 表单的dict可以禁用缓存
          url: '/api/basics_manage/customer_info/',
          value: 'id', // 数据字典中value字段的属性名
          label: 'name' // 数据字典中label字段的属性名
        },
        search: {
          disabled: false,
          key: 'customer_name',
          component: {
            name: 'el-input',
            placeholder: '请输入客户'
          }
        },
        form: {
          rules: [
            {
              required: true,
              message: '必填项',
              trigger: 'blur'
            }
          ],
          component: {
            span: 24,
            placeholder: '请选择客户',
            elProps: {
              tableConfig: {
                pagination: true,
                multiple: false,
                columns: [
                  {
                    prop: 'id',
                    label: '编号'
                  },
                  {
                    prop: 'name',
                    label: '客户名称'
                  }
                ]
              }
            }
          },
          itemProps: {
            class: { yxtInput: true }
          }
        },
        component: {
          name: 'foreignKey',
          valueBinding: 'customer_name',
          props: { color: 'auto' }
        } // 自动染色
      },
      {
        title: '状态',
        key: 'status',
        search: {
          disabled: false
        },
        width: 70,
        type: 'radio',
        dict: {
          data: BUTTON_STATUS_NUMBER
        },
        form: {
          value: 1,
          component: {
            span: 12
          },
          rules: [
            { required: true, message: '状态不能为空', trigger: 'blur' }
          ],
          itemProps: {
            class: { yxtInput: true }
          }
        }
      }
    ].concat(vm.commonEndColumns({
      update_datetime: { showTable: false },
      dept_belong_id: { showForm: true, showTable: true }
    }))
  }
}
