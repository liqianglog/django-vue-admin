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
      width: 210,
      fixed: 'right',
      view: false,
      edit: false,
      remove: false,
      custom: [
        {
          thin: true,
          text: '回传文件记录',
          size: 'small',
          type: 'primary',
          emit: 'onStatusLog'
        },
        {
          thin: true,
          text: '问题码记录',
          size: 'small',
          type: 'warning',
          emit: 'onErrorCode'
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
        title: '码包编号',
        key: 'code_package_no',
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
            placeholder: '请输入'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '赋码工单号',
        key: 'production_work_no',
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
            { required: true, message: '不能为空', trigger: 'blur' }
          ],
          component: {
            placeholder: '请输入'
          },
          itemProps: {
            class: { yxtInput: true }
          },
          valueChange (key, value, form, { getColumn, mode, component, immediate, getComponent }) {
            if (mode === 'add' && !form.code) {
              form.code = util.autoShortCreateCode()
            }
          },
          valueChangeImmediate: true
        }
      },
      {
        title: '检测工单号',
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
            { required: true, message: '不能为空', trigger: 'blur' }
          ],
          component: {
            placeholder: '请输入'
          },
          itemProps: {
            class: { yxtInput: true }
          },
          valueChange (key, value, form, { getColumn, mode, component, immediate, getComponent }) {
            if (mode === 'add' && !form.code) {
              form.code = util.autoShortCreateCode()
            }
          },
          valueChangeImmediate: true
        }
      },
      {
        title: '码包总数',
        key: 'total_number',
        minWidth: 100,
        search: {
          disabled: true
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
        type: 'number',
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
        type: 'number',
        search: {
          disabled: true
        },
        form: {
          disabled: true
        }
      },
      {
        title: '识别成功率',
        key: 'success_rate',
        type: 'number',
        minWidth: 140,
        component: {
          name: 'table-progress'
        }
      },
      {
        title: '未识别码数',
        key: 'unrecognized_num',
        minWidth: 100,
        type: 'number',
        search: {
          disabled: true
        },
        form: {
          disabled: true
        }
      }, {
        title: '不存在码数',
        key: 'code_not_exist_num',
        minWidth: 100,
        type: 'number',
        search: {
          disabled: true
        },
        form: {
          disabled: true
        }
      }, {
        title: '本检测包重码数',
        key: 'self_repetition_num',
        minWidth: 140,
        type: 'number',
        search: {
          disabled: true
        },
        form: {
          disabled: true
        }
      },
      {
        title: '本生产工单重码数',
        key: 'prod_repetition_num',
        minWidth: 140,
        type: 'number',
        search: {
          disabled: true
        },
        form: {
          disabled: true
        }
      },
      {
        title: '非本生产工单码数',
        key: 'prod_wrong_num',
        minWidth: 140,
        type: 'number',
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
      },
      {
        title: '检测状态',
        key: 'status',
        fixed: 'right',
        search: {
          disabled: false
        },
        width: 100,
        type: 'radio',
        dict: {
          data: [
            { value: 1, label: '待检测' },
            { value: 2, label: '检测中' },
            { value: 3, label: '暂停中' },
            { value: 4, label: '检测结束' },
            { value: 5, label: '检测异常' }
          ]
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
      dept_belong_id: { showForm: false, showTable: false }
    }))
  }
}
