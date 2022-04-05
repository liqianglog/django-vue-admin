/*
 * @创建文件时间: 2021-06-03 00:34:42
 * @Auther: 猿小天
 * @最后修改人: 猿小天
 * @最后修改时间: 2021-11-19 22:18:47
 * 联系Qq:1638245306
 * @文件介绍: 权限配置
 */
export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      tableType: 'vxe-table',
      rowKey: true,
      width: '100%',
      height: '100%' // 表格高度100%, 使用toolbar必须设置
    },
    rowHandle: {
      edit: {
        thin: true,
        text: '编辑',
        disabled () {
          return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: '删除',
        disabled () {
          return !vm.hasPermissions('Delete')
        }
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
      defaultSpan: 24, // 默认的表单 span
      width: '35%'
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
        disabled: true,
        component: {
          placeholder: '请输入关键字'
        }
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

      type: 'input',
      form: {
        rules: [ // 表单校验规则
          { required: true, message: '名称必填项' }
        ],
        component: {
          placeholder: '请输入名称'
        },
        itemProps: {
          class: { yxtInput: true }
        }
      }
    },
    {
      title: 'key值',
      key: 'value',
      sortable: true,
      search: {
        disabled: false
      },

      type: 'input',
      form: {
        rules: [ // 表单校验规则
          { required: true, message: 'key值必填项' }
        ],
        component: {
          placeholder: '请输入key值'
        },
        itemProps: {
          class: { yxtInput: true }
        }
      }
    },
    {
      title: '备注',
      key: 'description',
      show: false,
      search: {
        disabled: true
      },
      type: 'textarea',
      form: {
        component: {
          placeholder: '请输入内容',
          showWordLimit: true,
          maxlength: '200',
          props: {
            type: 'textarea'
          }
        }
      }
    }, {
      title: '创建人',
      show: false,
      width: 100,
      key: 'modifier_name',
      form: {
        disabled: true
      }
    },
    {
      title: '更新时间',
      key: 'update_datetime',
      width: 160,
      type: 'datetime',
      sortable: true,
      form: {
        disabled: true
      }
    },
    {
      title: '创建时间',
      key: 'create_datetime',
      width: 160,
      type: 'datetime',
      sortable: true,
      form: {
        disabled: true
      }
    }
    ]
  }
}
