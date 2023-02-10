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
      width: 120,
      fixed: 'right',
      view: false,
      edit: false,
      remove: false,
      custom: [
        {
          thin: true,
          text: '检测文件记录',
          size: 'small',
          type: 'primary',
          emit: 'onStatusLog'
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
      componentType: 'row'
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
        title: '码包总数',
        key: 'total_number',
        minWidth: 100,
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true
            }
          }
        },
        type: 'number',
        form: {
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            placeholder: '请输入码包总数'
          }
        }
      },
      {
        title: '识别码总数',
        key: 'need_number',
        minWidth: 100,
        search: {
          disabled: true
        },
        form: {
          disabled: true
        }
      },
      {
        title: '识别成功数',
        key: 'success_number',
        minWidth: 100,
        search: {
          disabled: true
        },
        form: {
          disabled: true
        }
      },
      {
        title: '识别错误数',
        key: 'error_number',
        minWidth: 100,
        search: {
          disabled: true
        },
        form: {
          disabled: true
        }
      }, {
        title: '产品名称',
        key: 'product_name',
        minWidth: 100,
        type: 'input'
      }, {
        title: '到货工厂',
        key: 'arrival_factory',
        minWidth: 100,
        type: 'input'
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
        }
      },
      {
        title: '生产设备',
        key: 'device_name',
        width: 160,
        type: 'input',
        search: {
          disabled: false,
          component: {
            placeholder: '请输入生产设备',
            props: {
              clearable: true
            }
          }
        }
      }
    ].concat(vm.commonEndColumns({
      update_datetime: { showTable: true },
      dept_belong_id: { showForm: false, showTable: false }
    }))
  }
}
