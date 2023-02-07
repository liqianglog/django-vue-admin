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
          disabled: false,
          component: {
            props: {
              clearable: true
            }
          }
        },
        form: {
          disabled: true,
          component: {
            placeholder: '请输入关键词',
            props: {
              clearable: true
            }
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
      },
      {
        title: '模板编号',
        key: 'no',
        minWidth: 80,
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
          rules: [
            { required: true, message: '模板编号不能为空', trigger: 'blur' }
          ],
          component: {
            placeholder: '请输入模板编号'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      }, {
        title: '分隔符',
        key: 'separator',
        search: {
          disabled: true
        },
        minWidth: 70,
        type: 'input',
        // dict: {
        //   data: [{ label: ',', value: ',' }, { label: '竖线', value: '|' }, { label: '分号', value: ';' }]
        // },
        form: {
          component: {
            placeholder: '分隔符',
            span: 12
          },
          rules: [
            { required: true, message: '分隔符不能为空', trigger: 'blur' }
          ],
          itemProps: {
            class: { yxtInput: true }
          }
        }
      }, {
        title: '换行符',
        key: 'line_feed',
        search: {
          disabled: true
        },
        minWidth: 110,
        type: 'select',
        dict: {
          data: [{ label: '回车换行(\\r\\n)', value: 1 }, { label: '换行(\\n)', value: 0 }]
        },
        form: {
          component: {
            span: 12
          },
          rules: [
            { required: true, message: '换行符不能为空', trigger: 'blur' }
          ],
          itemProps: {
            class: { yxtInput: true }
          }
        }
      }, {
        title: '字段数',
        key: 'fields',
        type: 'number',
        minWidth: 70,
        form: {
          component: {
            placeholder: '字段数',
            props: {
              min: 0
            }
          },
          rules: [
            { required: true, message: '字段数不能为空', trigger: 'blur' }
          ],
          itemProps: {
            class: { yxtInput: true }
          }
        }
      }, {
        title: '字符长度',
        key: 'char_length',
        type: 'number',
        minWidth: 80,
        form: {
          component: {
            placeholder: '字符长度',
            props: {
              min: 0
            }
          },
          rules: [
            { required: true, message: '字符长度不能为空', trigger: 'blur' }
          ],
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },{
        title: '码字段位置',
        key: 'code_position',
        type: 'number',
        minWidth: 120,
        form: {
          rules: [
            { required: true, message: '码字段位置不能为空', trigger: 'blur' }
          ],
          component: {
            placeholder: '码字段位置',
            props: {
              min: 0
            }
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      }, {
        title: '时间字段位置',
        key: 'time_position',
        type: 'number',
        minWidth: 120,
        form: {
          rules: [
            { required: true, message: '时间字段位置不能为空', trigger: 'blur' }
          ],
          component: {
            placeholder: '时间字段位置',
            props: {
              min: 0
            }
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      }
    ].concat(vm.commonEndColumns({
      update_datetime: { showTable: false },
      dept_belong_id: { showForm: false },
      description: { showForm: false }
    }))
  }
}
