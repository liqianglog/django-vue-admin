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
      width: 200,
      fixed: 'right',
      view: false,
      edit: false,
      remove: false,
      custom: [
        {
          thin: true,
          text: '生产状态记录',
          size: 'small',
          type: 'primary',
          emit: 'onStatusLog'
        },
        {
          thin: true,
          text: '生产报告',
          size: 'small',
          type: 'warning',
          emit: 'onProductionReport',
          disabled (_, form) {
            // return !(form.status === 4 || form.status === 5) && !vm.hasPermissions('ImportReport')
            return !vm.hasPermissions('ProductionReport')
          }
        }
      ]
    },
    // rowHandle: {
    //   fixed: 'right',
    //   view: {
    //     thin: true,
    //     text: '',
    //     disabled () {
    //       return !vm.hasPermissions('Retrieve')
    //     }
    //   },
    //   width: 140,
    //   edit: {
    //     thin: true,
    //     text: '',
    //     disabled () {
    //       return !vm.hasPermissions('Update')
    //     }
    //   },
    //   remove: {
    //     thin: true,
    //     text: '',
    //     disabled () {
    //       return !vm.hasPermissions('Delete')
    //     }
    //   }
    // },
    viewOptions: {
      componentType: 'form'
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
        title: 'ID',
        key: 'id',
        show: false,
        form: {
          disabled: true
        }
      },
      {
        title: '生产工单号',
        key: 'no',
        minWidth: 200,
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
            { required: true, message: '工厂编号不能为空', trigger: 'blur' }
          ],
          component: {
            placeholder: '请输入工厂编号'
          },
          itemProps: {
            class: { yxtInput: true }
          },
          valueChange (key, value, form, { getColumn, mode, component, immediate, getComponent }) {
            if (mode === 'add') {
              form.code = util.autoShortCreateCode()
            }
          },
          valueChangeImmediate: true
        }
      }, {
        title: '生产订单号',
        key: 'order_id',
        minWidth: 200,
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
            { required: true, message: '不能为空', trigger: 'blur' }
          ],
          component: {
            placeholder: '请输入生产订单号'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '生产码包',
        key: 'code_package',
        type: 'selector-table',
        minWidth: 120,
        dict: {
          cache: false, // 表单的dict可以禁用缓存
          url: '/api/carton/code_manage/code_package/?validate_status=4',
          value: 'id', // 数据字典中value字段的属性名
          label: 'no' // 数据字典中label字段的属性名
        },
        search: {
          disabled: false,
          key: 'code_package_no',
          component: {
            name: 'el-input',
            placeholder: '请输入码包编号'
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
            placeholder: '请选择码包',
            on: {
              // 单选事件
              radioChange ({ event }) {
                console.log(111, event)
              }
            },
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
                    prop: 'no',
                    label: '码包名称'
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
        title: '喷印模板',
        key: 'jet_print_template',
        type: 'selector-table',
        minWidth: 120,
        dict: {
          cache: false, // 表单的dict可以禁用缓存
          url: '/api/basics_manage/jet_print_template/',
          value: 'id', // 数据字典中value字段的属性名
          label: 'name' // 数据字典中label字段的属性名
        },
        search: {
          disabled: false,
          key: 'jet_print_template_name',
          component: {
            name: 'el-input',
            placeholder: '请输入喷印模板名称'
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
            placeholder: '请选择码包',
            on: {
              // 单选事件
              radioChange ({ event }) {
                console.log(111, event)
              }
            },
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
                    label: '喷印模板名称'
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
          valueBinding: 'jet_print_template_name',
          props: { color: 'auto' }
        } // 自动染色
      },
      {
        title: '批次号',
        key: 'batch_no',
        minWidth: 200,
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
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            placeholder: '请输入批次号'
          }
        }
      }, {
        title: '打印位置',
        key: 'print_position',
        minWidth: 100,
        type: 'number',
        form: {
          addDisabled: true,
          editDisabled: true
        }
      }, {
        title: '生产工厂',
        key: 'factory_info_name',
        width: 180,
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
          addDisabled: true,
          editDisabled: true,
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            placeholder: '请输入生产工厂'
          }
        }
      },
      {
        title: '生产产线',
        key: 'production_line_name',
        width: 160,
        type: 'input',
        search: {
          disabled: false,
          component: {
            placeholder: '请输入生产产线',
            props: {
              clearable: true
            }
          }
        },
        form: {
          addDisabled: true,
          editDisabled: true
        }
      },
      {
        title: '生产设备',
        key: 'device',
        type: 'selector-table',
        minWidth: 120,
        dict: {
          cache: false, // 表单的dict可以禁用缓存
          url: '/api/basics_manage/device_manage/',
          value: 'id', // 数据字典中value字段的属性名
          label: 'name' // 数据字典中label字段的属性名
        },
        search: {
          disabled: false,
          key: 'device_name',
          component: {
            name: 'el-input',
            placeholder: '请输入设备名称'
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
            placeholder: '请选择设备',
            on: {
              // 单选事件
              radioChange (context) {
                const { event, scope } = context
                scope.form.factory_info = event.factory_id
                scope.form.production_line = event.production_line
              }
            },
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
                    label: '设备名称'
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
          valueBinding: 'device_name',
          props: { color: 'auto' }
        } // 自动染色
      },
      {
        title: '生产状态',
        key: 'status',
        fixed: 'right',
        search: {
          disabled: false
        },
        width: 100,
        type: 'radio',
        dict: {
          data: [
            { value: 0, label: '待下载' },
            { value: 1, label: '待生产' },
            { value: 2, label: '生产中' },
            { value: 3, label: '暂停中' },
            { value: 4, label: '结束生产' },
            { value: 5, label: '工单异常' },
            { value: 6, label: '码包下载成功' }
          ]
        },
        form: {
          addDisabled: true,
          editDisabled: true,
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
      update_datetime: { showTable: true },
      dept_belong_id: { showForm: false, showTable: false }
    }))
  }
}
