import { urlPrefix as factoryInfoUrlPrefix } from '../factoryInfo/api'
import { request } from '@/api/service'
import { urlPrefix as productionLineUrlPrefix } from '../productionLine/api'

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
      fixed: 'right',
      view: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      width: 160,
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
      defaultSpan: 24, // 默认的表单 span
      width: '35%'
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
        title: '设备名称',
        key: 'name',
        width: 140,
        search: {
          disabled: true
        },
        type: 'input',
        form: {
          rules: [
            { required: true, message: '设备名称不能为空', trigger: 'blur' }
          ],
          component: {
            placeholder: '请输入设备名称'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '设备编号',
        key: 'no',
        width: 200,
        search: {
          disabled: false
        },
        type: 'input',
        form: {
          disabled: true,
          component: {
            placeholder: '请输入设备编号'
          }
        }
      },
      {
        title: '登录密码',
        key: 'password',
        width: 100,
        search: {
          disabled: true
        },
        type: 'input',
        form: {
          disabled: true,
          rules: [
            { required: true, message: '登录密码不能为空', trigger: 'blur' }
          ],
          component: {
            placeholder: '请输入登录密码'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '归属工厂',
        key: 'factory_info',
        width: 150,
        type: 'table-selector',
        dict: {
          cache: false, // 表单的dict可以禁用缓存
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
        search: {
          disabled: false
        },
        form: {
          rules: [ // 表单校验规则
            { required: true, message: '归属工厂必填项' }
          ],
          component: {
            props: {
              multiple: false,
              clearable: true,
              pagination: true
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
            placeholder: '请先选择归属工厂'
          },
          itemProps: {
            class: { yxtInput: true }
          },
          valueChange (key, value, form, { getColumn, mode, component, immediate, getComponent }) {
            if (value) {
              var selected = getComponent(key) && getComponent(key).selected[0]
              if (selected) {
                getComponent('production_line').reloadDict()
              }
            }
          }
        },
        component: {
          name: 'foreignKey',
          valueBinding: 'factory_name'
        }
      },
      {
        title: '归属产线',
        key: 'production_line',
        type: 'table-selector',
        width: 150,
        dict: {
          cache: false, // 表单的dict可以禁用缓存
          url: productionLineUrlPrefix + '?status=1',
          value: 'id', // 数据字典中value字段的属性名
          label: 'name', // 数据字典中label字段的属性名
          getData: (url, dict, { form, component }) => {
            return request({ url: url, params: { page: 1, limit: 10, belong_to_factory: form.factory_info } }).then(ret => {
              component._elProps.page = ret.data.page
              component._elProps.limit = ret.data.limit
              component._elProps.total = ret.data.total
              return ret.data.data
            })
          }
        },
        search: {
          disabled: false
        },
        form: {
          rules: [ // 表单校验规则
            { required: true, message: '必填项归属产线' }
          ],
          component: {
            props: {
              multiple: false,
              clearable: true
            },
            placeholder: '请选择归属产线',
            elProps: {
              pagination: true,
              columns: [
                {
                  field: 'code',
                  title: '编号'
                },
                {
                  field: 'name',
                  title: '产线名称'
                },
                {
                  field: 'belong_to_factory_name',
                  title: '工厂名称'
                }
              ]
            }
          },
          itemProps: {
            class: { yxtInput: true }
          }
        },
        component: {
          name: 'foreignKey',
          valueBinding: 'production_line_name'
        }
      }, {
        title: '设备类型',
        key: 'type',
        search: {
          disabled: false
        },
        width: 150,
        type: 'select',
        dict: {
          data: [{ label: '检测管理端', value: 1 }, { label: '码包管理端', value: 0 }]
        },
        form: {
          value: 0,
          component: {},
          rules: [
            { required: true, message: '设备类型不能为空', trigger: 'blur' }
          ],
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '设备状态',
        key: 'production_status',
        search: {
          disabled: false
        },
        width: 100,
        type: 'radio',
        dict: {
          data: [{ label: '维护中', value: 2 }, { label: '生产中', value: 1 }, { label: '闲置中', value: 0 }]
        },
        form: {
          value: 0,
          component: {},
          rules: [
            { required: true, message: '状态不能为空', trigger: 'blur' }
          ],
          itemProps: {
            class: { yxtInput: true }
          }
        }
      }
    ].concat(vm.commonEndColumns({}))
  }
}
