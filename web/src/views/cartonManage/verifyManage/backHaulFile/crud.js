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
      width: 240,
      fixed: 'right',
      view: false,
      edit: false,
      remove: false,
      custom: [
        {
          thin: true,
          text: '下载文件',
          size: 'small',
          type: 'primary',
          emit: 'onDownload',
          disabled (_, form) {
            return !vm.hasPermissions('Download')
          }
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
        title: '文件名称',
        key: 'file_name',
        minWidth: 220,
        search: {
          disabled: true
        },
        type: 'input',
        form: {
          disabled: true
        }
      }, {
        title: '赋码工单号',
        key: 'production_work_no',
        minWidth: 180,
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
        minWidth: 120,
        search: {
          disabled: true
        },
        form: {
          disabled: true
        }
      },
      {
        title: '相机编号',
        key: 'cam_no',
        minWidth: 120,
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
        minWidth: 120,
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
        minWidth: 120,
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
        title: '识别错误数',
        key: 'error_number',
        minWidth: 120,
        search: {
          disabled: true
        },
        form: {
          disabled: true
        }
      },
      {
        title: '未识别码数',
        key: 'undfind_number',
        minWidth: 100,
        search: {
          disabled: true
        },
        form: {
          disabled: true
        }
      }, {
        title: '不存在码数',
        key: 'inexistence_number',
        minWidth: 100,
        search: {
          disabled: true
        },
        form: {
          disabled: true
        }
      }, {
        title: '本检测包重码数',
        key: 'self_repetition_number',
        minWidth: 140,
        search: {
          disabled: true
        },
        form: {
          disabled: true
        }
      },
      {
        title: '本生产工单重码数',
        key: 'prod_repetition_number',
        minWidth: 140,
        search: {
          disabled: true
        },
        form: {
          disabled: true
        }
      },
      {
        title: '非本生产工单码数',
        key: 'prod_undfind_number',
        minWidth: 140,
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
