import util from '@/libs/util'

const uploadUrl = util.baseURL() + 'api/carton/code_manage/code_package/upload_file/'
export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    pagination: false,
    options: {
      tableType: 'vxe-table',
      rowKey: true, // 必须设置，true or false
      rowId: 'id',
      height: '100%', // 表格高度100%, 使用toolbar必须设置
      highlightCurrentRow: false
    },
    rowHandle: {
      fixed: 'right',
      width: 260,
      view: {
        thin: true,
        text: '',
        size: 'small',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      edit: false,
      remove: {
        thin: true,
        text: '',
        size: 'small',
        disabled (_, form) {
          return !vm.hasPermissions('Delete') || form.validate_status === 4
        }
      },
      custom: [
        {
          thin: true,
          text: '导入日志',
          size: 'small',
          type: 'primary',
          emit: 'onOrderLog',
          disabled (_, form) {
            return !vm.hasPermissions('ImportLog') && form.validate_status === 4
          }
        },
        {
          thin: true,
          text: '导入报告',
          size: 'small',
          type: 'warning',
          emit: 'onImportLog',
          disabled (_, form) {
            return !(form.validate_status === 3 || form.validate_status === 4) && !vm.hasPermissions('ImportReport')
          }
        }
      ]
    },
    viewOptions: {
      componentType: 'form'
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
        title: '订单号',
        key: 'order_id',
        search: {
          disabled: false
        },
        type: 'input',
        width: 200,
        form: {
          rules: [ // 表单校验规则
            {
              required: true,
              message: '必填项'
            },
            {
              pattern: /^[A-Za-z0-9_-]{4,40}$/,
              message: '格式为:字母、数字、-、_;至少4位;最多40位'
            }
          ],
          component: {
            placeholder: '请输入订单号',
            span: 24,
            props: {
              clearable: true
            }
          },
          itemProps: {
            class: { yxtInput: true }
          },
          helper: {
            render (h) {
              return (< el-alert title="如有实际订单号，请重新输入" type="warning"/>
              )
            }
          }
        }
      },
      {
        title: '码包文件',
        key: 'file_path',
        // type: 'image-uploader',
        type: 'file-uploader',
        width: 150,
        align: 'left',
        show: false,
        form: {
          rules: [ // 表单校验规则
            {
              required: true,
              message: '请上传码包文件'
            }
          ],
          component: {
            props: {
              uploader: {
                action: uploadUrl,
                name: 'file',
                headers: {
                  Authorization: 'JWT ' + util.cookies.get('token')
                },
                type: 'form',
                successHandle (ret, option) {
                  if (ret.code !== 2000) {
                    throw new Error('上传失败')
                  }
                  // return {
                  //   file_path: ret.data.data.file_path, key: option.data.key, no: ret.data.data.no, name: ret.data.data.name, file_type: ret.data.data.file_type, is_encrypted: ret.data.data.is_encrypted
                  // }
                  return ret.data.data
                }
              },
              returnType: 'object',
              elProps: { // 与el-uploader 配置一致
                multiple: false,
                limit: 1, // 限制1个文件
                beforeUpload (file) {
                  const fileName = file.name
                  // 获取最后一个.的位置
                  const index = fileName.lastIndexOf('.')
                  // 获取后缀
                  const ext = fileName.substr(index + 1)
                  // 输出结果
                  if (ext === 'txt' || ext === 'zip') {
                    return true
                  } else {
                    vm.$message.error('文件格式不正确')
                    return false
                  }
                }
              }
              // sizeLimit: 50 * 1024 // 不能超过限制
            },
            span: 24
          },
          itemProps: {
            class: { yxtInput: true }
          },
          valueChange (key, value, form) { // 当返回值有变化时触发
            if (value != null) {
              form.zip_name = value.name
              form.file_type = value.file_type
              vm.is_encrypted = value.is_encrypted
            }
          },
          helper: '只能上传 zip / txt 后缀文件'
        },
        valueResolve (row, col) {
          const value = row[col.key]
          if (value != null && value instanceof Array) {
            if (value.length >= 0) {
              row[col.key] = value
            } else {
              row[col.key] = null
            }
          } else {
            if (value instanceof Object) {
              row[col.key] = value.file_path
            } else {
              row[col.key] = value
            }
          }
        }
      }, {
        title: '文件密码',
        key: 'pwd',
        show: false,
        type: 'input',
        form: {
          rules: [ // 表单校验规则
            {
              required: true,
              message: '必填项'
            }
          ],
          component: {
            placeholder: '请输入',
            span: 24,
            showPassword: true,
            props: {
              clearable: true
            },
            show (context) {
              return vm.is_encrypted
            }
          },
          itemProps: {
            class: { yxtInput: true }
          },
        }
      },
      {
        title: '关联客户',
        key: 'customer_info',
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
            span: 24,
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
          },
          valueChange (key, value, form, { getColumn, mode, component, immediate, getComponent }) {
            // form表单数据change事件，表单值有改动将触发此事件
            if (value) {
              vm.isAttrShow = true
              vm.getCusomerInfoAttr(value)
              form.product_info = null
              getComponent('product_info').reloadDict()
            } else {
              vm.isAttrShow = false
            }
          },
          valueChangeImmediate: false
        },
        component: {
          name: 'foreignKey',
          valueBinding: 'customer_name',
          props: { color: 'auto' }
        } // 自动染色
      },
      {
        title: '关联产品',
        key: 'product_info',
        type: 'selector-table',
        minWidth: 120,
        dict: {
          cache: false, // 表单的dict可以禁用缓存
          // url: '/api/basics_manage/product_info/',
          url (dict, { form, component }) {
            if (form && form.customer_info != null) { // 本数据字典的url是通过前一个select的选项决定的
              return '/api/basics_manage/product_info/?customer_info=' + form.customer_info
            }
            return undefined // 返回undefined 将不加载字典
          },
          value: 'id', // 数据字典中value字段的属性名
          label: 'name' // 数据字典中label字段的属性名
        },
        search: {
          disabled: false,
          key: 'product_name',
          component: {
            name: 'el-input',
            placeholder: '请输入产品'
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
            show(){
              return vm.isAttrShow
            },
            span: 24,
            placeholder: '请选择产品',
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
                    label: '产品名称'
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
          valueBinding: 'product_name',
          props: { color: 'auto' }
        } // 自动染色
      },
      {
        title: '生产工厂',
        key: 'factory_info',
        type: 'selector-table',
        minWidth: 120,
        dict: {
          cache: false, // 表单的dict可以禁用缓存
          url: '/api/basics_manage/factory_info/',
          value: 'id', // 数据字典中value字段的属性名
          label: 'name' // 数据字典中label字段的属性名
        },
        search: {
          disabled: false,
          key: 'factory_name',
          component: {
            name: 'el-input',
            placeholder: '请输入工厂名称'
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
            span: 24,
            placeholder: '请选择工厂',
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
                    label: '工厂名称'
                  }
                ]
              }
            }
          },
          itemProps: {
            class: { yxtInput: true }
          },
        },
        component: {
          name: 'foreignKey',
          valueBinding: 'factory_name',
          props: { color: 'auto' }
        } // 自动染色
      },
      {
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
            span: 24,
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
          },
        },
        component: {
          name: 'foreignKey',
          valueBinding: 'code_package_template_name',
          props: { color: 'auto' }
        } // 自动染色
      },
      {
        title: '码包总数',
        key: 'total_number',
        type: 'number',
        width: 120,
        form: {
          disabled: true
        }
      }, {
        title: '本码包重码数',
        key: 'package_repetition_number',
        type: 'number',
        width: 100,
        form: {
          disabled: true
        }
      },
      {
        title: '历史码包重码数',
        key: 'database_repetition_number',
        type: 'number',
        width: 120,
        form: {
          disabled: true
        }
      },
      {
        title: '压缩包名称',
        key: 'zip_name',
        type: 'input',
        width: 260,
        form: {
          disabled: true
        }
      },
      {
        title: '码包编号',
        key: 'no',
        type: 'input',
        width: 260,
        form: {
          disabled: true
        }
      }, {
        title: '来源',
        key: 'source_label',
        type: 'input',
        width: 80,
        form: {
          disabled: true
        }
      },
      {
        title: '校验状态',
        key: 'validate_status',
        type: 'select',
        fixed: 'right',
        width: 100,
        dict: {
          data: [
            { value: 1, label: '待校验' },
            { value: 2, label: '校验中' },
            { value: 3, label: '校验失败' },
            { value: 4, label: '校验成功' }
          ]
        },
        search: {
          disabled: true,
          component: {
            placeholder: '请选择校验状态'
          }
        },
        form: {
          disabled: true
        }
      },
      {
        title: '检测完成时间',
        key: 'import_end_datetime',
        width: 160,
        type: 'datetime',
        form: {
          disabled: true
        }
      },
      {
        title: '检测耗时(秒)',
        key: 'import_run_time',
        width: 100,
        type: 'number',
        form: {
          disabled: true
        }
      },
      {
        title: '其他字段属性',
        key: 'attribute_fields',
        type: 'input',
        form: {
          component: {
            show () { return vm.isAttrShow },
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
      create_datetime: { showTable: true },
      update_datetime: { showTable: false },
      dept_belong_id: { showForm: false, showTable: false }
    }))
  }
}
