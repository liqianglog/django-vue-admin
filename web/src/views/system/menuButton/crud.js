/*
 * @创建文件时间: 2021-06-03 00:50:28
 * @Auther: 猿小天
 * @最后修改人: 猿小天
 * @最后修改时间: 2021-07-29 22:49:02
 * 联系Qq:1638245306
 * @文件介绍: 菜单的按钮和接口配置
 */
import { request } from '@/api/service'
export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      tableType: 'vxe-table',
      rowKey: false,
      width: '100%',
      height: '100%' // 表格高度100%, 使用toolbar必须设置
    },
    rowHandle: {
      width: 180,
      edit: {
        thin: true,
        text: '编辑'
      },
      remove: {
        thin: true,
        text: '删除'
      }
    },
    indexRow: { // 或者直接传true,不显示title，不居中
      title: '序号',
      align: 'center',
      width: 100
    },
    viewOptions: {
      disabled: true,
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 24 // 默认的表单 span
    },
    columns: [{
      title: '关键词',
      key: 'search',
      show: false,
      disabled: true,
      search: {
        disabled: false
      },
      form: {
        disabled: true
      },
      view: { // 查看对话框组件的单独配置
        disabled: true
      }
    },
    {
      title: 'ID',
      key: 'id',
      show: false,
      width: 90,
      form: {
        disabled: true
      }
    },

    {
      title: '名称',
      key: 'name',
      sortable: true,
      search: {
        disabled: false
      },
      type: 'select',
      dict: {
        cache: false,
        url: '/api/system/button/',
        label: 'name',
        value: 'name',
        getData: (url, dict) => {
          return request({ url: url }).then(ret => {
            return ret.data.data
          })
        }
      },
      form: {
        rules: [ // 表单校验规则
          { required: true, message: '必填项' }
        ],
        component: {
          span: 10
        },
        itemProps: {
          class: { yxtInput: true }
        },
        valueChange (key, value, form, { getColumn, mode, component, immediate, getComponent }) {
          if (value != null) {
            const obj = component.dictOptions.find(item => {
              return item.name === value
            })
            form.value = obj.value
          }
        }
      }
    },
    {
      title: '',
      key: 'createBtn',
      type: 'button',
      show: false,
      search: {
        disabled: true
      },
      form: {
        slot: true,
        component: {
          span: 2
        },
        itemProps: {
          labelWidth: '0px' // 可以隐藏表单项的label
        }
      }

    },
    {
      title: '权限值',
      key: 'value',

      show: false,
      sortable: true,
      search: {
        disabled: true
      },
      type: 'input',
      form: {
        disabled: true,
        show: false,
        rules: [ // 表单校验规则
          { required: true, message: '必填项' }
        ],
        component: {
          span: 12
        },
        itemProps: {
          class: { yxtInput: true }
        }
      }
    },
    {
      title: '请求方式',
      key: 'method',
      sortable: true,
      search: {
        disabled: false
      },
      type: 'select',
      dict: {
        data: [
          { label: 'GET', value: 0 },
          { label: 'POST', value: 1 },
          { label: 'PUT', value: 2 },
          { label: 'DELETE', value: 3 }
        ]
      },
      form: {
        rules: [ // 表单校验规则
          { required: true, message: '必填项' }
        ],
        component: {
          span: 12
        },
        itemProps: {
          class: { yxtInput: true }
        }
      }
    },
    {
      title: '接口地址',
      key: 'api',
      sortable: true,
      search: {
        disabled: true
      },
      type: 'select',
      dict: {
        url: '/swagger.json',
        label: 'label',
        value: 'value',
        getData: (url, dict) => {
          return request({ url: url }).then(ret => {
            const res = Object.keys(ret.paths)
            const data = []
            for (const item of res) {
              const obj = {}
              obj.label = item
              obj.value = item
              data.push(obj)
            }

            return data
          })
        }
      },
      form: {
        rules: [ // 表单校验规则
          { required: true, message: '必填项' }
        ],
        component: {
          span: 24,
          props: {
            elProps: {
              allowCreate: true,
              filterable: true,
              clearable: true
            }

          }
        },
        itemProps: {
          class: { yxtInput: true }
        },
        helper: {
          render (h) {
            return (< el-alert title="请正确填写，以免请求时被拦截。匹配单例使用正则,例如:/api/xx/.*?/" type="warning" />
            )
          }
        }
      }
    }
    ]
  }
}
