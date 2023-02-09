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
      remove: false,
      custom:[
        {
          thin: true,
          text: '下载文件',
          size: 'small',
          type: 'primary',
          emit: 'onDownload',
          disabled (_, form) {
            return !vm.hasPermissions('Download')
          }
        }
      ]
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
        title: '生产工单号',
        key: 'production_work_no',
        search: {
          disabled: true
        },
        type: 'input',
        form: {
          disabled: true
        }
      },
      {
        title: '码类型',
        key: 'code_type',
        width: 100,
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
            { value: 0, label: '内码' },
            { value: 1, label: '外码' },
            { value: 2, label: '未知' }
          ]
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
        key: 'cam_name',
        search: {
          disabled: true
        },
        form: {
          disabled: true
        }
      },
      {
        title: '码包总数',
        key: 'total_number',
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
        component: {
          name: 'table-progress'
        }
      },
      {
        title: '识别错误数',
        key: 'error_number',
        search: {
          disabled: true
        },
        form: {
          disabled: true
        }
      }
    ]
  }
}
