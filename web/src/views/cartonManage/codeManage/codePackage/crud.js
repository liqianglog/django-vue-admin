
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
    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 12 // 默认的表单 span
    },
    indexRow: { // 或者直接传true,不显示title，不居中
      title: '序号',
      align: 'center',
      width: 100
    },
    columns: [
      {
        title: '订单号',
        key: 'order_id',
        search: {
          disabled: false
        },
        type: 'input',
        form: {
          rules: [ // 表单校验规则
            {
              required: true,
              message: '必填项'
            },
            {
              pattern: /^[A-Za-z0-9]{4,40}$/,
              message: '格式为:字母、数字'
            }
          ],
          component: {
            span: 24,
            props: {
              clearable: true
            }
          },
          valueChange (key, value, form, {
            getColumn,
            mode,
            component,
            immediate,
            getComponent
          }) {
            if (value) {
              form.id = value
            } else {
              form.id = util.autoCreateCode()
            }
          },
          valueChangeImmediate: true,
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
            row[col.key] = value.file_path
          }
        }
      },
      {
        title: '产品名称',
        key: 'product_name',
        search: {
          disabled: false
        },
        type: 'input',
        form: {
          rules: [ // 表单校验规则
            {
              required: true,
              message: '必填项'
            }
          ],
          component: {
            placeholder: '请输入产品名称',
            span: 24,
            props: {
              clearable: true
            }
          }
        }
      },
      {
        title: '到货工厂',
        key: 'arrival_factory',
        search: {
          disabled: false
        },
        type: 'input',
        form: {
          rules: [ // 表单校验规则
            {
              required: true,
              message: '必填项'
            }
          ],
          component: {
            placeholder: '请输入到货工厂',
            span: 24,
            props: {
              clearable: true
            }
          }
        }
      },
      {
        title: '码包模板',
        key: 'code_package_template',
        search: {
          disabled: false
        },
        type: 'select',
        dict: {
          url: '/api/basics_manage/code_package_template/',
          label: 'no',
          value: 'id'
        },
        form: {
          rules: [ // 表单校验规则

            {
              required: true,
              message: '必填项'
            }
          ],
          component: {
            placeholder: '请选择码包模板',
            span: 24,
            props: {
              clearable: true
            }
          }
        }
      },
      {
        title: '文件密码',
        key: 'pwd',
        search: {
          disabled: false
        },
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
            props: {
              clearable: true
            },
            show (context) {
              return vm.is_encrypted
            }
          }
        }
      }
    ]
  }
}
