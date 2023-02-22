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
<!--          <el-button size="small" type="primary" v-permission="'Create'" @click="addRow"><i class="el-icon-plus"/> 新增</el-button>-->
        </el-button-group>
        <crud-toolbar :search.sync="crud.searchOptions.show"
                      :compact.sync="crud.pageOptions.compact"
                      :columns="crud.columns"
                      @refresh="doRefresh()"
                      @columns-filter-changed="handleColumnsFilterChanged"/>

      </div>
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
export default {
  name: 'productionWork',
  mixins: [d2CrudPlus.crud],
  components: {
    ProductionReport,
    statusLog
  },
  data () {
    return {
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
    }
  }
}
</script>
