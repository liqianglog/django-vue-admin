import { BUTTON_STATUS_NUMBER } from '@/config/button'
import { request } from '@/api/service'
import { urlPrefix as factoryInfoUrlPrefix } from '../factoryInfo/api'
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
      view: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      width: 140,
      edit: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Delete')
        }
      }
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
        title: '产线编号',
        key: 'code',
        width: 120,
        search: {
          disabled: false
        },
        type: 'input',
        form: {

          rules: [
            { required: true, message: '产线编号不能为空', trigger: 'blur' }
          ],
          component: {
            placeholder: '请输入产线编号'
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
      },
      {
        title: '产线名称',
        key: 'name',
        search: {
          disabled: false
        },
        form: {
          rules: [
            { required: true, message: '产线名称不能为空', trigger: 'blur' }
          ],
          component: {
            placeholder: '请输入产线名称'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '归属工厂',
        key: 'belong_to_factory',
        type: 'table-selector',
        search: {
          disabled: false
        },
        dict: {
          cache: true,
          url: factoryInfoUrlPrefix + '?status=1',
          value: 'id', // 数据字典中value字段的属性名
          label: 'name', // 数据字典中label字段的属性名
          getData: (url, dict, { form, component }) => {
            return request({ url: url, params: { page: 1, limit: 10 } }).then(ret => {
              component._elProps.page = ret.data.page
              component._elProps.limit = ret.data.limit
              component._elProps.total = ret.data.total
              return ret.data.data
            })
          }
        },
        form: {
          rules: [ // 表单校验规则
            { required: true, message: '必填项归属工厂' }
          ],
          component: {
            on: { // 单选事件监听
              radioChange ({ event, scope }) {
                scope.form.dept_belong_id = event.row.dept_belong_id
              }
            },
            props: {
              multiple: false,
              pagination: true,
              clearable: true
            },
            elProps: {
              pagination: true,
              columns: [
                {
                  field: 'name',
                  title: '工厂名称'
                },
                {
                  field: 'contacts',
                  title: '联系人'
                },
                {
                  field: 'telephone',
                  title: '联系电话'
                }
              ]
            },
            placeholder: '请选择归属工厂'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        },
        component: {
          name: 'foreignKey',
          valueBinding: 'belong_to_factory_name'
        }
      },
      {
        title: '状态',
        key: 'status',
        search: {
          disabled: false
        },
        type: 'radio',
        dict: {
          data: BUTTON_STATUS_NUMBER
        },
        form: {
          value: 1,
          component: {},
          rules: [
            { required: true, message: '不能为空', trigger: 'blur' }
          ],
          itemProps: {
            class: { yxtInput: true }
          }
        }
      }
    ].concat(vm.commonEndColumns({ dept_belong_id: { showForm: true, showTable: true } }))
  }
}
