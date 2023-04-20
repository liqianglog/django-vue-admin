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
      defaultSpan: 24, // 默认的表单 span
      width: '700px'
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
        title: '关联码包模板',
        key: 'code_package_template',
        type: 'selector-table',
        minWidth: 120,
        dict: {
          cache: false, // 表单的dict可以禁用缓存
          url: '/api/basics_manage/code_package_template/',
          value: 'id', // 数据字典中value字段的属性名
          label: 'name' // 数据字典中label字段的属性名
        },
        search: {
          disabled: false,
          key: 'code_package_template_name',
          component: {
            name: 'el-input',
            placeholder: '请输入码包模板名称'
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
            placeholder: '请选择码包模板',
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
                    label: '模板名称'
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
          valueBinding: 'code_package_template_name',
          props: { color: 'auto' }
        } // 自动染色
      }, {
        title: '排版样图',
        key: 'img',
        type: 'avatar-uploader',
        minWidth: 100,
        search: {
          disabled: true
        },
        form: {
          component: {
            props: {
              clearable: true
            },
            placeholder: '请选择提交图片'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      }, {
        title: '每张纸箱数',
        key: 'carton_number',
        type: 'number',
        minWidth: 70,
        form: {

          component: {

            placeholder: '纸箱数',
            props: {
              min: 0
            }
          },
          rules: [
            { required: true, message: '纸箱数不能为空', trigger: 'blur' }
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
          addDisabled: true, // 是否仅在添加编辑框中关闭该字段
          editDisabled: true, // 是否仅在修改编辑框中关闭该字段
          component: {
            disabled: true,
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
