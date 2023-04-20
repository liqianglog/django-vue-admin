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
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 12, // 默认的表单 span
      width: '900px'
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
        minWidth: 100,
        search: {
          disabled: true,
          component: {
            props: {
              clearable: true
            }
          }
        },
        type: 'input',
        form: {
          rules: [
            { required: true, message: '不能为空', trigger: 'blur' }
          ],
          component: {
            placeholder: '请输入编号'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      }, {
        title: '模板名称',
        key: 'name',
        minWidth: 100,
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
            { required: true, message: '模板名称不能为空', trigger: 'blur' }
          ],
          component: {
            placeholder: '请输入模板名称'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      }, {
        title: '归属客户',
        key: 'customer',
        type: 'selector-table',
        minWidth: 120,
        dict: {
          cache: false, // 表单的dict可以禁用缓存
          url: '/api/basics_manage/customer_info/',
          value: 'id', // 数据字典中value字段的属性名
          label: 'name' // 数据字典中label字段的属性名
        },
        search: {
          disabled: false,
          key: 'customer_name',
          component: {
            name: 'el-input',
            placeholder: '请输入客户'
          }
        },
        form: {
          rules: [
            {
              required: true,
              message: '必填项',
              trigger: 'blur'
            }
          ],
          component: {
            placeholder: '请选择客户',
            elProps: {
              tableConfig: {
                pagination: true,
                multiple: false,
                columns: [
                  {
                    prop: 'id',
                    label: '编号'
                  },
                  {
                    prop: 'name',
                    label: '客户名称'
                  }
                ]
              }
            }
          },
          itemProps: {
            class: { yxtInput: true }
          }
        },
        component: {
          name: 'foreignKey',
          valueBinding: 'customer_name',
          props: { color: 'auto' }
        } // 自动染色
      }, {
        title: '换行符',
        key: 'line_feed',
        search: {
          disabled: true
        },
        minWidth: 110,
        type: 'select',
        dict: {
          data: [{ label: '回车换行(\\r\\n)', value: 2 }, { label: '换行(\\n)', value: 1 }]
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
          },
          helper: {
            render (h) {
              return (< el-alert type="warning" description="文本中每行结尾所使用的符号"/>
              )
            }
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
          },
          helper: {
            render (h) {
              return (< el-alert type="warning" description="文本中每行包含换行符的字符长度"/>
              )
            }
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
        form: {
          component: {
            dict: {
              data: [{ label: ',', value: ',' }, { label: '|', value: '|' }, { label: ';', value: ';' }, { label: '无', value: '无' }]
            },
            name: 'dict-select',
            span: 12
          },
          rules: [
            { required: true, message: '分隔符不能为空', trigger: 'blur' }
          ],
          itemProps: {
            class: { yxtInput: true }
          },
          helper: {
            render (h) {
              return (< el-alert type="warning" description="文本中对字段进行分隔的符号"/>
              )
            }
          }
        }
      }, {
        title: '字段数',
        key: 'fields',
        type: 'number',
        minWidth: 70,
        form: {
          // addDisabled: true, //是否仅在添加编辑框中关闭该字段
          // editDisabled: true, //是否仅在修改编辑框中关闭该字段
          component: {
            disabled: true,
            placeholder: '字段数',
            props: {
              min: 0
            }
          },
          value: 1,
          // rules: [
          //   { required: true, message: '字段数不能为空', trigger: 'blur' }
          // ],
          itemProps: {
            class: { yxtInput: true }
          },
          helper: {
            render (h) {
              return (< el-alert type="warning" description="文本中每行通过分隔符分隔后的数量,根据字段属性默认生成"/>
              )
            }
          }
        }
      },
      {
        title: '字段属性',
        key: 'attr_fields',
        type: 'input',
        form: {
          component: {
            span: 24
          },
          itemProps: {
            class: { yxtInput: true }
          },
          slot: true
        },
        show: false// 不在单元格显示
      }
    ].concat(vm.commonEndColumns({
      update_datetime: { showTable: false },
      dept_belong_id: { showForm: false },
      description: { showForm: false }
    }))
  }
}
