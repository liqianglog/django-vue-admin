import { getButtonSettings } from '@/config/button'

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
    rowHandle: false,
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
        key: 'production_work_no',
        minWidth: 220,
        search: {
          disabled: true,
          component: {
            props: {
              clearable: true
            }
          }
        },
        type: 'input'
      },
      {
        title: '码包订单号',
        key: 'order_id',
        minWidth: 200,
        search: {
          disabled: true,
          component: {
            props: {
              clearable: true
            }
          }
        },
        type: 'input'
      },
      {
        title: '码类型',
        key: 'code_type',
        width: 120,
        search: {
          disabled: false,
          component: {
            placeholder: '请选择码类型',
            props: {
              clearable: true
            }
          }
        },
        type: 'select',
        dict: {
          data: [
            { value: 0, label: '外码' },
            { value: 1, label: '内码' },
            { value: 2, label: '外码+内码' }
          ]
        }
      },
      {
        title: '校验码内容集合',
        key: 'code_list',
        minWidth: 270,
        rowSlot: true,
        search: {
          disabled: true,
          component: {
            props: {
              clearable: true
            }
          }
        },
        type: 'input'
      },
      {
        title: '生产工厂',
        key: 'factory_info_name',
        width: 140,
        search: {
          disabled: false,
          component: {
            placeholder: '请输入生产工厂',
            props: {
              clearable: true
            }
          }
        },
        type: 'input'
      },
      {
        title: '生产产线',
        key: 'production_line_name',
        width: 140,
        search: {
          disabled: false,
          component: {
            placeholder: '请输入生产产线',
            props: {
              clearable: true
            }
          }
        },
        type: 'input'
      },
      {
        title: '生产设备',
        key: 'device_name',
        width: 140,
        search: {
          disabled: false,
          component: {
            placeholder: '请输入生产设备',
            props: {
              clearable: true
            }
          }
        },
        type: 'input'
      }, {
        title: '校验结果',
        key: 'result',
        width: 120,
        fixed: 'right',
        search: {
          disabled: false,
          component: {
            placeholder: '请选择校验结果',
            props: {
              clearable: true
            }
          }
        },
        type: 'select',
        dict: {
          data: getButtonSettings([
            { value: 0, label: '失败' },
            { value: 1, label: '成功' }
          ])
        }
      },
      {
        title: '记录时间',
        key: 'record_datetime',
        width: 160,
        fixed: 'right',
        search: {
          disabled: true,
          component: {
            placeholder: '请选择记录时间',
            props: {
              clearable: true
            }
          }
        },
        type: 'datetime'
      }
    ]
  }
}
