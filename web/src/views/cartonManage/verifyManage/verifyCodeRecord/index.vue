<template>
  <d2-container  :class="{'page-compact':crud.pageOptions.compact}">
    <d2-crud-x
        ref="d2Crud"
        v-bind="_crudProps"
        v-on="_crudListeners"
    >
      <div slot="header">
        <el-tabs v-model="activeName" @tab-click="handleClick">
          <el-tab-pane label="全部" name="9"></el-tab-pane>
          <el-tab-pane label="未识别" name="0"></el-tab-pane>
          <el-tab-pane label="码不存在" name="2"></el-tab-pane>
          <el-tab-pane label="本检测包重码" name="3"></el-tab-pane>
          <el-tab-pane label="本生产工单重码" name="4"></el-tab-pane>
          <el-tab-pane label="非本生产工单码" name="5"></el-tab-pane>
        </el-tabs>
        <crud-search ref="search" :options="crud.searchOptions" @submit="handleSearch"  />
        <el-button-group>
<!--          <el-button size="small" type="primary" v-permission="'Create'" @click="addRow"><i class="el-icon-plus"/> 新增</el-button>-->
          <el-button
            size="small"
            type="warning"
            @click="onExport"
            v-permission="'Export'"
          ><i class="el-icon-download" /> 导出
          </el-button>
        </el-button-group>
        <crud-toolbar :search.sync="crud.searchOptions.show"
                      :compact.sync="crud.pageOptions.compact"
                      :columns="crud.columns"
                      @refresh="doRefresh()"
                      @columns-filter-changed="handleColumnsFilterChanged"/>

      </div>
    </d2-crud-x>

  </d2-container>
</template>

<script>
import * as api from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
export default {
  name: 'verifyCodeRecord',
  mixins: [d2CrudPlus.crud],
  data () {
    return {
      activeName: '9'
    }
  },
  methods: {
    getCrudOptions () {
      return crudOptions(this)
    },
    handleClick () {
      this.doRefresh({ from: 'load' })
    },
    pageRequest (query) {
      if (this.activeName !== '9') {
        query.error_type = this.activeName
      }
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
    onExport () {
      const that = this
      that.$confirm('是否确认导出所有数据项?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(function () {
        const query = that.getSearch().getForm()
        return api.exportData({ ...query })
      })
    }
  }
}
</script>
