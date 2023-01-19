<!--
 * @创建文件时间: 2021-08-02 22:53:41
 * @Auther: 猿小天
 * @最后修改人: 猿小天
 * @最后修改时间: 2021-08-23 23:05:56
 * 联系Qq:1638245306
 * @文件介绍:
-->
<template>
   <d2-crud-x ref="d2Crud" v-bind="_crudProps" v-on="_crudListeners">
      <div slot="header">
        <crud-search
          ref="search"
          :options="crud.searchOptions"
          @submit="handleSearch"
        />
        <!-- <el-button-group>
          <el-button size="small" type="primary" @click="addRow"
            ><i class="el-icon-plus" /> 新增</el-button
          >
        </el-button-group> -->
        <crud-toolbar
          :search.sync="crud.searchOptions.show"
          :compact.sync="crud.pageOptions.compact"
          :columns="crud.columns"
          @refresh="doRefresh()"
          @columns-filter-changed="handleColumnsFilterChanged"
        />
      </div>
    </d2-crud-x>
</template>

<script>
import * as api from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
export default {
  name: 'taskDetail',
  mixins: [d2CrudPlus.crud],
  props: {
    detailsInfo: {
      type: Object,
      default: () => {}
    }
  },
  watch: {
    detailsInfo () {
      this.doRefresh({ from: 'load' })
    }
  },
  data () {
    return {}
  },
  methods: {
    getCrudOptions () {
      return crudOptions(this)
    },
    pageRequest (query) {
      const params = {
        ...query,
        job: this.detailsInfo.job_id,
        periodic_task_name: this.detailsInfo.name
      }
      return api.GetList(params)
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
    }
  }
}
</script>
