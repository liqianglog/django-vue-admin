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
      width: '500px',
      defaultSpan: 24 // 默认的表单 span
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
        form: {
          component: {
            dict: {
              data: [{ label: '无', value: '无' }, { label: ',', value: ',' }, { label: '|', value: '|' }, {
                label: ';',
                value: ';'
              }]
            },
            name: 'dict-select',
            placeholder: '分隔符'
          },
          rules: [
            { required: true, message: '分隔符不能为空', trigger: 'blur' }
          ],
          valueChange (key, value) {
            if (value === '无') {
              vm.showAcTime = false
            } else {
              vm.showAcTime = true
            }
          },
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
        minWidth: 110,
        type: 'select',
        dict: {
          data: [{ label: '回车换行(\\r\\n)', value: 1 }, { label: '换行(\\n)', value: 0 }]
        },
        form: {
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
      },
      // {
      //   title: '字段数',
      //   key: 'fields',
      //   type: 'number',
      //   minWidth: 70,
      //   form: {
      //     component: {
      //       placeholder: '字段数',
      //       props: {
      //         min: 0
      //       }
      //     },
      //     rules: [
      //       { required: true, message: '字段数不能为空', trigger: 'blur' }
      //     ],
      //     itemProps: {
      //       class: { yxtInput: true }
      //     }
      //   }
      // },
      // {
      //   title: '字符长度',
      //   key: 'char_length',
      //   type: 'number',
      //   minWidth: 80,
      //   form: {
      //     component: {
      //       placeholder: '字符长度',
      //       props: {
      //         min: 0
      //       }
      //     },
      //     rules: [
      //       { required: true, message: '字符长度不能为空', trigger: 'blur' }
      //     ],
      //     itemProps: {
      //       class: { yxtInput: true }
      //     }
      //   }
      // },
      {
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
          },
          helper: {
            render (h) {
              return (< el-alert type="warning" description="文本中每行通过分隔符分隔后的位置下标,默认从0开始"/>
              )
            }
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
            show () {
              return vm.showAcTime
            },
            placeholder: '时间字段位置',
            props: {
              min: 0
            }
          },
          itemProps: {
            class: { yxtInput: true }
          },
          helper: {
            render (h) {
              return (< el-alert type="warning" description="文本中每行通过分隔符分隔后的位置下标,默认从0开始"/>
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
