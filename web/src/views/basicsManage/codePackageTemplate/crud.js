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
        title: '版号',
        key: 'code_version',
        minWidth: 80,
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
            { required: true, message: '版号不能为空', trigger: 'blur' }
          ],
          component: {
            placeholder: '请输入版号'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      }, {
        title: '编码来源',
        key: 'code_source',
        search: {
          disabled: false,
          component: {
            props: {
              clearable: true
            }
          }
        },
        width: 100,
        type: 'select',
        dict: {
          data: [{ label: '信码新创', value: 1 }, { label: '透云平台', value: 0 }, { label: '其他', value: 2 }]
        },
        form: {
          value: 1,
          component: {
            span: 12
          },
          rules: [
            { required: true, message: '编码来源不能为空', trigger: 'blur' }
          ],
          itemProps: {
            class: { yxtInput: true }
          }
        }
      }, {
        title: '码类型',
        key: 'code_type',
        search: {
          disabled: false
        },
        width: 110,
        type: 'select',
        dict: {
          data: [{ label: '外码+内码', value: 2 }, { label: '内码', value: 1 }, { label: '外码', value: 0 }]
        },
        form: {
          component: {
            span: 12
          },
          rules: [
            { required: true, message: '码类型不能为空', trigger: 'blur' }
          ],
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
        width: 70,
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
        title: '换行符',
        key: 'line_feed',
        search: {
          disabled: true
        },
        width: 110,
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
          },
          helper: {
            render (h) {
              return (< el-alert type="warning" description="文本中每行结尾所使用的符号"/>
              )
            }
          }
        }
      }, {
        title: '字段数',
        key: 'fields',
        type: 'number',
        width: 70,
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
          },
          helper: {
            render (h) {
              return (< el-alert type="warning" description="文本中每行通过分隔符分隔后的数量"/>
              )
            }
          }
        }
      }, {
        title: '字符长度',
        key: 'char_length',
        type: 'number',
        width: 80,
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
              return (< el-alert type="warning" description="文本中每行不包含换行符的字符长度"/>
              )
            }
          }
        }
      }, {
        title: '外码地址',
        key: 'w_url_prefix',
        minWidth: 180,
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
            { required: true, message: '外码地址不能为空', trigger: 'blur' }
          ],
          component: {
            placeholder: '请输入外码地址'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      }, {
        title: '内码地址',
        key: 'n_url_prefix',
        minWidth: 180,
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
            { required: true, message: '内码地址不能为空', trigger: 'blur' }
          ],
          component: {
            placeholder: '请输入内码地址'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      }, {
        title: '外码内容长度',
        key: 'w_url_length',
        type: 'number',
        width: 100,
        form: {
          value: 0,
          rules: [
            { required: true, message: '外码内容长度不能为空', trigger: 'blur' }
          ],
          component: {
            placeholder: '外码内容长度',
            props: {
              min: 0
            }
          },
          itemProps: {
            class: { yxtInput: true }
          },
          helper: {
            render (h) {
              return (< el-alert type="warning" description="文本中每行最后一个 '/' 后所有字符长度,默认从0开始"/>
              )
            }
          }
        }
      }, {
        title: '内码内容长度',
        key: 'n_url_length',
        type: 'number',
        width: 100,
        form: {
          value: 0,
          rules: [
            { required: true, message: '内码长度不能为空', trigger: 'blur' }
          ],
          component: {
            placeholder: '内码长度',
            props: {
              min: 0
            }
          },
          itemProps: {
            class: { yxtInput: true }
          },
          helper: {
            render (h) {
              return (< el-alert type="warning" description="文本中每行最后一个 '/' 后所有字符长度,默认从0开始"/>
              )
            }
          }
        }
      }, {
        title: '外码位置',
        key: 'w_field_position',
        type: 'number',
        width: 80,
        form: {
          rules: [
            { required: true, message: '外码位置不能为空', trigger: 'blur' }
          ],
          component: {
            placeholder: '外码位置',
            props: {
              min: 0
            }
          },
          itemProps: {
            class: { yxtInput: true }
          },
          helper: {
            render (h) {
              return (< el-alert type="warning" description="外码所占字段数的下标位置,默认从0开始"/>
              )
            }
          }
        }
      }, {
        title: '内码位置',
        key: 'n_field_position',
        type: 'number',
        width: 80,
        form: {
          rules: [
            { required: true, message: '内码位置不能为空', trigger: 'blur' }
          ],
          component: {
            placeholder: '内码位置',
            props: {
              min: 0
            }
          },
          itemProps: {
            class: { yxtInput: true }
          },
          helper: {
            render (h) {
              return (< el-alert type="warning" description="内码所占字段数的下标位置,默认从0开始"/>
              )
            }
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
