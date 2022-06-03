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
          // return !vm.hasPermissions('Retrieve')
        }
      },
      width: 230,
      edit: {
        thin: true,
        text: '',
        disabled () {
          // return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: '',
        disabled () {
          // return !vm.hasPermissions('Delete')
        }
      },
      custom: [{
        show (index, row) {
          return true
        },
        disabled () {
          // return !vm.hasPermissions('Update')
        },
        text: '作品设计',
        type: 'warning',
        size: 'small',
        emit: 'workDesign'
      }]

    },
    indexRow: { // 或者直接传true,不显示title，不居中
      title: '序号',
      align: 'center',
      width: 100
    },

    viewOptions: {
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
          props: {
            clearable: true
          },
          placeholder: '请输入关键词'
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
      title: '标题',
      key: 'title',
      sortable: true,
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
        rules: [ // 表单校验规则
          { required: true, message: '标题必填项' }
        ],
        component: {
          props: {
            clearable: true
          },
          placeholder: '请输入标题'
        },
        itemProps: {
          class: { yxtInput: true }
        }
      }
    },
    {
      title: '封面图片',
      key: 'cover_image_url',
      type: 'image-uploader',
      sortable: true,
      form: {
        rules: [ // 表单校验规则
          { required: true, message: '封面图片必填项' }
        ],
        component: {
          props: {
            clearable: true
          },
          placeholder: '请输入封面图片'
        },
        itemProps: {
          class: { yxtInput: true }
        }
      }
    },
    {
      title: '是否发布',
      key: 'is_publish',
      sortable: true,
      type: 'radio',
      dict: {
        data: vm.dictionary('button_whether_bool')
      },
      form: {
        value: false,
        component: {
          placeholder: '请选择是是否发布'
        }
      }
    }, {
      title: '是否模板',
      key: 'is_template',
      sortable: true,
      type: 'radio',
      dict: {
        data: vm.dictionary('button_whether_bool')
      },
      form: {
        value: false,
        component: {
          placeholder: '请选择是是否模板'
        }
      }
    }
    ].concat(vm.commonEndColumns({
      description: {
        showForm: true,
        showTable: true
      }
    }))
  }
}
