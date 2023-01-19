<!--
 * @创建文件时间: 2021-08-02 22:53:41
 * @Auther: 猿小天
 * @最后修改人: 猿小天
 * @最后修改时间: 2021-08-23 22:22:32
 * 联系Qq:1638245306
 * @文件介绍:
-->
<template>
  <d2-container :class="{ 'page-compact': crud.pageOptions.compact }">
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @toDetail="toDetail"
    >
      <div slot="header">
        <crud-search
          ref="search"
          :options="crud.searchOptions"
          @submit="handleSearch"
        />
        <el-button-group>
          <el-button size="small" type="primary" @click="addRow"
            ><i class="el-icon-plus" /> 新增</el-button
          >
        </el-button-group>
        <crud-toolbar
          :search.sync="crud.searchOptions.show"
          :compact.sync="crud.pageOptions.compact"
          :columns="crud.columns"
          @refresh="doRefresh()"
          @columns-filter-changed="handleColumnsFilterChanged"
        />
      </div>

      <template slot="crontabSlot" slot-scope="scope">
        <el-tag size="mini">{{scope.row['crontab']}}</el-tag>
      </template>
    </d2-crud-x>

    <el-drawer
      :title="'来自定时任务' + detailsInfo.name"
      :visible.sync="detailsDrawer"
      size="70%"
    >
      <TaskDetails :detailsInfo="detailsInfo" />
    </el-drawer>
  </d2-container>
</template>

<script>
import * as api from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
import TaskDetails from '../taskDetail/index.vue'

export default {
  name: 'task',
  mixins: [d2CrudPlus.crud],

  components: {
    TaskDetails
  },
  data () {
    return {
      detailsDrawer: false,
      detailsInfo: {}
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
      return api.AddObj(row)
    },
    updateRequest (row) {
      return api.UpdateObj(row)
    },
    delRequest (row) {
      return api.DelObj(row)
    },
    // 开关任务
    onSwitchTask ({ row }) {
      api.UpdateStatus(row).then((ret) => {
        this.$message.success(ret.msg)
      })
      this.getD2CrudTableData()
    },
    // 定时任务详情
    toDetail ({ row }) {
      this.detailsDrawer = true
      this.detailsInfo = row
    }
  }
}
</script>
