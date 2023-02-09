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
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      width: 140,
      edit: false,
      remove: false
    },
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
      }, {
        title: 'ID',
        key: 'id',
        show: false,
        form: {
          disabled: true
        }
      }, {
        title: '相机编号',
        key: 'no',
        search: {
          disabled: true
        },
        type: 'input',
        form: {
          disabled: true
        }
      },
      {
        title: '设备名称',
        key: 'device_name',
        search: {
          disabled: true
        },
        form: {
          disabled: true
        }
      },
      {
        title: '工厂名称',
        key: 'factory_name',
        search: {
          disabled: true
        },
        form: {
          disabled: true
        }
      },
      {
        title: '产线名称',
        key: 'prod_line_name',
        search: {
          disabled: true
        },
        form: {
          disabled: true
        }
      },
      {
        title: '总码数',
        key: 'total_number',
        type: 'number'
      },
      {
        title: '识别成功数',
        key: 'success_number',
        type: 'number'
      },
      {
        title: '识别失败数',
        key: 'error_number',
        type: 'number'
      },
      {
        title: '成功采集率',
        key: 'success_rate',
        type: 'number',
        component: {
          name: 'table-progress'
        }
      }
    ]
  }
}
