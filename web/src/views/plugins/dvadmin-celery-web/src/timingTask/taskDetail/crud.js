/*
 * @创建文件时间: 2021-08-22 09:45:19
 * @Auther: 猿小天
 * @最后修改人: 猿小天
 * @最后修改时间: 2021-08-23 23:06:13
 * 联系Qq:1638245306
 * @文件介绍:
 */
export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%'
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
    rowHandle: false,
    columns: [
      {
        title: '任务状态',
        key: 'status',
        sortable: true,
        search: {
          disabled: true
        },
        type: 'input',
        form: {
          component: {
            span: 12
          }
        }
      },
      {
        title: '开始时间',
        key: 'date_created',
        disabled: false,
        search: {
          disabled: false,
          width: 360,
          component: { // 查询框组件配置，默认根据form配置生成
            name: 'el-date-picker',
            props: {
              type: 'datetimerange',
              'range-separator': '至',
              'start-placeholder': '开始',
              'end-placeholder': '结束',
              'default-time': ['00:00:00', '23:59:59'],
              valueFormat: 'yyyy-MM-dd HH:mm:ss'
            }
          }
        },
        // 提交时,处理数据
        valueResolve (row, col) {
          if (row[col.key] instanceof Array) {
            row[col.key] = row[col.key].join(',')
          }
        },
        type: 'datetime'
      },
      {
        title: '运行时长(秒)',
        key: 'date_done',
        disabled: true,
        search: {
          disabled: true
        },
        type: 'number'

      },
      {
        title: '完成时间',
        key: 'date_done',
        search: {
          disabled: false,
          component: { // 查询框组件配置，默认根据form配置生成
            name: 'el-date-picker',
            props: {
              valueFormat: 'yyyy-MM-dd HH:mm:ss'
            }
          }
        },
        type: 'datetime'

      },
      {
        title: '结果',
        key: 'result',
        search: {
          disabled: true
        },
        type: 'input'
      }
    ]
  }
}
