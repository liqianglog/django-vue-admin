<template>
  <el-drawer
    :visible.sync="drawer"
    direction="rtl"
    :title="title"
    :size="1200"
  >
    <div slot="title">
      <span>回传文件名称</span>
      <el-tag size="small" style="margin-left: 10px">{{
          options.file_name
        }}</el-tag>
    </div>
    <div>
      <d2-container  style="margin-left: 10px;margin-top: 80px" :class="{ 'page-compact': crud.pageOptions.compact }">
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
<!--          <crud-toolbar :search.sync="crud.searchOptions.show"-->
<!--                        :compact.sync="crud.pageOptions.compact"-->
<!--                        :columns="crud.columns"-->
<!--                        @refresh="doRefresh()"-->
<!--                        @columns-filter-changed="handleColumnsFilterChanged"/>-->

        </div>
      </d2-crud-x>
      </d2-container>
    </div>
  </el-drawer>
</template>

<script>
import { d2CrudPlus } from 'd2-crud-plus'
import { crudOptions } from './crud'
import * as api from './api'
export default {
  mixins: [d2CrudPlus.crud],
  data () {
    return {
      activeName: '9',
      drawer: false,
      title: '问题码记录',
      options: {}
    }
  },
  watch: {
    options () {
      this.doRefresh({ from: 'load' })
    }
  },
  methods: {
    doLoad () {
    },
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
      return api.GetList({ ...query, back_haul_file: this.options.id, exclude_success: true })
    }
  }
}
</script>

<style scoped>

</style>
