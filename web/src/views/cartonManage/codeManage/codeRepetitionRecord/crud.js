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
        title: '重码订单编号',
        key: 'code_package_order_id',
        width: 200,
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
        title: '重码码包编号',
        key: 'code_package_no',
        width: 240,
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
        title: '码内容',
        key: 'code_content',
        width: 320,
        search: {
          disabled: false,
          width: 300,
          component: {
            placeholder: '请输入码内容',
            props: {
              clearable: true
            }
          }
        },
        type: 'input'
      },
      {
        title: '被重码订单编号',
        key: 'repetition_code_package_id',
        width: 200,
        search: {
          disabled: false,
          component: {
            placeholder: '请输入被重码码包',
            props: {
              clearable: true
            }
          }
        },
        type: 'input'
      },
      {
        title: '被重码码包编号',
        key: 'repetition_code_package_no',
        width: 240,
        search: {
          disabled: false,
          component: {
            placeholder: '请输入被重码码包',
            props: {
              clearable: true
            }
          }
        },
        type: 'input'
      },
      {
        title: '重码类型',
        key: 'repetition_type',
        width: 100,
        fixed: 'right',
        search: {
          disabled: false,
          component: {
            placeholder: '请选择重码类型',
            props: {
              clearable: true
            }
          }
        },
        type: 'select',
        dict: {
          data: [
            { value: 0, label: '码包重码' },
            { value: 1, label: '历史重码' }
          ]
        }
      },
      {
        title: '重码时间',
        key: 'create_datetime',
        width: 160,
        fixed: 'right',
        search: {
          disabled: true,
          width: 240,
          component: { // 查询框组件配置，默认根据form配置生成
            name: 'el-date-picker',
            props: {
              type: 'daterange',
              'range-separator': '至',
              'start-placeholder': '开始',
              'end-placeholder': '结束',
              valueFormat: 'yyyy-MM-dd'
            }
          }
        },
        type: 'datetime',
        sortable: true,
        form: {
          disabled: false
        }
      }
    ]
  }
}
