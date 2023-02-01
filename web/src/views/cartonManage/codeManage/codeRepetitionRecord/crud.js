import { BUTTON_STATUS_NUMBER } from '@/config/button'
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
        title: '码包',
        key: 'code_package',
        width: 120,
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
        width: 200,
        search: {
          disabled: false,
          component: {
            placeholder: '请输入码内容',
            props: {
              clearable: true
            }
          }
        },
        type: 'input'
      }, {
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
        dist: {
          data: [
            { value: 0, label: '外码' },
            { value: 1, label: '内码' },
            { value: 2, label: '外码+内码' }
          ]
        }
      },
      {
        title: '重码码包',
        key: 'repetition_code_package',
        width: 100,
        search: {
          disabled: false,
          component: {
            placeholder: '请输入重码码包',
            props: {
              clearable: true
            }
          }
        },
        type: 'input'
      },
      {
        title: '重码码类型',
        key: 'repetition_type',
        width: 100,
        search: {
          disabled: false,
          component: {
            placeholder: '请选择重码码类型',
            props: {
              clearable: true
            }
          }
        },
        type: 'select',
        dist: {
          data: [
            { value: 0, label: '外码' },
            { value: 1, label: '内码' },
            { value: 2, label: '外码+内码' }
          ]
        }
      }
    ].concat(vm.commonEndColumns({
      update_datetime: { showTable: false },
      dept_belong_id: { showForm: false, showTable: false }
    }))
  }
}
