<template>
  <el-drawer
    :visible.sync="drawer"
    direction="rtl"
    :title="title"
    size="50%"
  >
    <div slot="title">
      <span>生产工单</span>
      <el-tag size="small" style="margin-left: 10px">{{
          options.no
        }}</el-tag>
    </div>
    <div>
      <d2-crud-x
        ref="d2Crud"
        v-bind="_crudProps"
        v-on="_crudListeners"
      >
        <div slot="header">
          <crud-search ref="search" :options="crud.searchOptions" @submit="handleSearch"  />
<!--          <crud-toolbar :search.sync="crud.searchOptions.show"-->
<!--                        :compact.sync="crud.pageOptions.compact"-->
<!--                        :columns="crud.columns"-->
<!--                        @refresh="doRefresh()"-->
<!--                        @columns-filter-changed="handleColumnsFilterChanged"/>-->

        </div>
      </d2-crud-x>
    </div>
  </el-drawer>
</template>

<script>
import { d2CrudPlus } from 'd2-crud-plus'
import { crudOptions } from './crud'
import * as api from '@/views/cartonManage/productionManage/productionWorkStatusRecord/api'
export default {
  mixins: [d2CrudPlus.crud],
  data () {
    return {
      drawer: false,
      title:"生产状态记录",
      options:{}
    }
  },
  methods: {
    getCrudOptions () {
      return crudOptions(this)
    },
    pageRequest (query) {
      return api.GetList(query)
    }
  }
}
</script>

<style scoped>

</style>
