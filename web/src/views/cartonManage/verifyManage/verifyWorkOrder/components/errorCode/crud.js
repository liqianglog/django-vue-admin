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
        title: '码内容',
        key: 'code_content',
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
            { value: 0, label: '外码' },
            { value: 1, label: '内码' },
            { value: 2, label: '外码+内码' }
          ]
        }
      },
      {
        title: '采集时间',
        key: 'ac_time',
        search: {
          disabled: true
        },
        form: {
          disabled: true
        }
      },
      {
        title: '重码次数',
        key: 'rep_code_number',
        search: {
          disabled: true
        },
        form: {
          disabled: true
        }
      },
      {
        title: '问题码类型',
        key: 'error_type',
        type: 'select',
        dict: {
          data: [
            { value: 0, label: '未识别' },
            { value: 1, label: '正常' },
            { value: 2, label: '码不存在' },
            { value: 3, label: '本码包重码' },
            { value: 4, label: '历史码重码' },
            { value: 5, label: '非生产工单码' }
          ]
        },
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