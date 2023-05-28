<template>
  <d2-container  :class="{'page-compact':crud.pageOptions.compact}">
    <d2-crud-x
        ref="d2Crud"
        v-bind="_crudProps"
        v-on="_crudListeners"
        @onStatusLog="onStatusLog"
        @onProductionReport="onProductionReport"
    >
      <div slot="header">
        <crud-search ref="search" :options="crud.searchOptions" @submit="handleSearch"  />
        <el-button-group>
          <el-button size="small" type="primary" v-permission="'Create'" @click="addRow"><i class="el-icon-plus"/> 新增</el-button>
        </el-button-group>
        <crud-toolbar :search.sync="crud.searchOptions.show"
                      :compact.sync="crud.pageOptions.compact"
                      :columns="crud.columns"
                      @refresh="doRefresh()"
                      @columns-filter-changed="handleColumnsFilterChanged"/>

      </div>
<!--      码包展示-->
      <template slot="code_package_displayFormSlot" slot-scope="scope">
        <div style="border: 1px solid #DCDFE6;padding-left: 15px;border-radius: 5px">
        <div  v-if="scope.form.code_package">
          <div>码包名称:{{code_package_displayForm.zip_name}}</div>
          <div>码包订单号:{{code_package_displayForm.order_id}}</div>
          <div>客户名称:{{code_package_displayForm.customer_name}}</div>
          <div>产品名称:{{code_package_displayForm.product_name}}</div>
          <div>码包模板名称:{{code_package_displayForm.code_package_template_name}}</div>
        </div>
        <div v-else>请选择码包</div>
        </div>
      </template>
    </d2-crud-x>
    <statusLog ref="statusLog"></statusLog>
    <production-report ref="productionReport"></production-report>
  </d2-container>
</template>

<script>
import * as api from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
import statusLog from './components/productionWorkStatusRecord'
import ProductionReport from '@/views/cartonManage/productionManage/productionWork/components/productionReport'
import util from '@/libs/util'
export default {
  name: 'productionWork',
  mixins: [d2CrudPlus.crud],
  components: {
    ProductionReport,
    statusLog
  },
  data () {
    return {
      code_package_displayForm: {
        zip_name: '',
        order_id: '',
        customer_name: '',
        product_name: '',
        code_package_template_name: ''

      }
    }
  },
  methods: {
    getCrudOptions () {
      return crudOptions(this)
    },
    pageRequest (query) {
      return api.GetList(query)
    },
    addRequest (row) {
      return api.createObj(row)
    },
    updateRequest (row) {
      return api.UpdateObj(row)
    },
    delRequest (row) {
      return api.DelObj(row.id)
    },
    // 生产状态日志
    onStatusLog ({ row }) {
      this.$refs.statusLog.options = row
      this.$refs.statusLog.drawer = true
    },
    // 生产报告
    onProductionReport ({ row }) {
      this.$refs.productionReport.options = row
      this.$refs.productionReport.drawer = true
      this.$refs.productionReport.getInit()
    },
    // 监听表单打开事件,给自定义字段赋值
    handleDialogOpened ({ mode, form, template, groupTemplate }) {
      if (mode === 'add' && !form.no) {
        form.no = util.autoShortCreateCode()
      }
    }
  }
}
</script>
