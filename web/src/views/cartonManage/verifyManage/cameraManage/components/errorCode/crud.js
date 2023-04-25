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
        title: '明码内容',
        key: 'error_code_content',
        minWidth: 200,
        search: {
          disabled: true
        },
        type: 'input',
        form: {
          disabled: true
        }
      },
      {
        title: 'MD5码内容',
        key: 'code_content_md5',
        minWidth: 200,
        search: {
          disabled: true
        },
        type: 'input',
        form: {
          disabled: true
        }
      },
      {
        title: '问题码类型',
        key: 'error_type',
        type: 'select',
        fixed: 'right',
        width: 120,
        dict: {
          data: [
            { value: 0, label: '未识别' },
            { value: 1, label: '正常' },
            { value: 2, label: '码不存在' },
            { value: 3, label: '本检测包重码' },
            { value: 4, label: '本生产工单重码' },
            { value: 5, label: '非本生产工单码' }
          ]
        },
        search: {
          disabled: true
        },
        form: {
          disabled: true
        }
      },
      {
        title: '采集时间',
        key: 'ac_time',
        fixed: 'right',
        width: 150,
        search: {
          disabled: true
        },
        form: {
          disabled: true
        }
      },
      {
        title: '相机编号',
        key: 'camera_no',
        width: 100,
        type: 'input',
        search: {
          disabled: true,
          component: {
            placeholder: '请输入',
            props: {
              clearable: true
            }
          }
        }
      },
      {
        title: '码包编号',
        key: 'code_package_no',
        width: 200,
        type: 'input',
        search: {
          disabled: true,
          component: {
            placeholder: '请输入',
            props: {
              clearable: true
            }
          }
        }
      },
      {
        title: '生产工单',
        key: 'production_work_no',
        width: 180,
        type: 'input',
        search: {
          disabled: true,
          component: {
            placeholder: '请输入',
            props: {
              clearable: true
            }
          }
        }
      },
      {
        title: '检测工单',
        key: 'verify_work_no',
        width: 180,
        type: 'input',
        search: {
          disabled: true,
          component: {
            placeholder: '请输入',
            props: {
              clearable: true
            }
          }
        }
      },
      {
        title: '回传文件名称',
        key: 'file_name',
        width: 200,
        type: 'input',
        search: {
          disabled: true,
          component: {
            placeholder: '请输入',
            props: {
              clearable: true
            }
          }
        }
      },
      {
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
    ]
  }
}
