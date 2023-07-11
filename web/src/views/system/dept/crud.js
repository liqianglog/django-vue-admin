import * as api from './api'
export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    pagination: false,
    options: {
      tableType: 'vxe-table',
      stripe: false,
      rowKey: true, // 必须设置，true or false
      rowId: 'id',
      height: '100%', // 表格高度100%, 使用toolbar必须设置
      highlightCurrentRow: false,
      defaultExpandAll: true,
      resizable: true,
      treeConfig: {
        transform: true,
        rowField: 'id',
        parentField: 'parent',
        hasChild: 'hasChild',
        lazy: true,
        loadMethod: ({ row }) => {
          let query = JSON.parse(JSON.stringify(vm.getSearch().getForm()))
          query = Object.fromEntries(
            Object.entries(query).filter(([_, value]) => ![undefined, null, [], '[]', ''].includes(value))
          )
          query.parent = row.id
          // console.log(query)
          return api.GetList({ ...query }).then(ret => {
            return ret.data.data
          })
        },
        iconLoaded: 'el-icon-loading' // 美化loading图标
      }
    },
    rowHandle: {
      fixed: 'right',
      width: 140,
      view: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
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
    indexRow: {
      // 或者直接传true,不显示title，不居中
      title: '序号',
      align: 'center',
      width: 70
    },

    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 12 // 默认的表单 span
    },
    columns: [
      {
        title: '关键词',
        key: 'search',
        show: false,
        disabled: true,
        search: {
          disabled: true
        },
        form: {
          disabled: true,
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入关键词'
          }
        },
        view: {
          // 查看对话框组件的单独配置
          disabled: true
        }
      },
      {
        title: 'ID',
        key: 'id',
        show: false,
        disabled: true,
        width: 90,
        form: {
          disabled: true
        }
      },
      {
        show: false,
        title: '上级部门',
        key: 'parent',
        type: 'tree-selector',
        minWidth: 200,
        dict: {
          isTree: true,
          label: 'name',
          value: 'id',
          cache: false,
          getData: (url, dict, { form, component }) => { // 配置此参数会覆盖全局的getRemoteDictFunc
            return api.DeptLazy().then(ret => { return ret })
          }
        },
        form: {
          helper: '默认留空为创建者的部门',
          component: {
            span: 12,
            props: {
              multiple: false
            }
          }
        }
      },
      {
        title: '部门名称',
        key: 'name',
        sortable: true,
        treeNode: true, // 设置为树形列
        minWidth: 180,
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true
            }
          }
        },
        type: 'input',
        showOverflow: 'tooltip',
        form: {
          rules: [
            // 表单校验规则
            { required: true, message: '部门名称必填项' }
          ],
          component: {
            span: 12,
            props: {
              clearable: true
            },
            placeholder: '请输入部门名称'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '部门标识',
        key: 'key',
        sortable: true,
        minWidth: 100,
        form: {
          component: {
            props: {
              clearable: true
            },
            placeholder: '请输入标识字符'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '负责人',
        key: 'owner',
        sortable: true,
        minWidth: 100,
        form: {
          component: {
            span: 12,
            props: {
              clearable: true
            },
            placeholder: '请输入负责人'
          }
        }
      },
      {
        title: '联系电话',
        key: 'phone',
        sortable: true,
        minWidth: 100,
        form: {
          component: {
            span: 12,
            props: {
              clearable: true
            },
            placeholder: '请输入联系电话'
          }
        }
      },
      {
        title: '邮箱',
        key: 'email',
        sortable: true,
        minWidth: 100,
        form: {
          component: {
            span: 12,
            props: {
              clearable: true
            },
            placeholder: '请输入邮箱'
          },
          rules: [
            {
              type: 'email',
              message: '请输入正确的邮箱地址',
              trigger: ['blur', 'change']
            }
          ]
        }
      },
      {
        title: '排序',
        key: 'sort',
        sortable: true,
        width: 80,
        type: 'number',
        form: {
          value: 1,
          component: {
            span: 12,
            placeholder: '请选择序号'
          }
        }
      },
      {
        title: '状态',
        key: 'status',
        sortable: true,
        search: {
          disabled: false
        },
        width: 90,
        type: 'radio',
        dict: {
          data: vm.dictionary('button_status_bool')
        },
        form: {
          value: true,
          component: {
            span: 12,
            placeholder: '请选择状态'
          }
        }
      }
    ].concat(vm.commonEndColumns())
  }
}
