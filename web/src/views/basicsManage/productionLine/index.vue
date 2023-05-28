<template>
  <d2-container  :class="{'page-compact':crud.pageOptions.compact}">
    <d2-crud-x
        ref="d2Crud"
        v-bind="_crudProps"
        v-on="_crudListeners"
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
    </d2-crud-x>

  </d2-container>
</template>

<script>
import * as api from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
import { request } from '@/api/service'
import util from '@/libs/util'
export default {
  name: 'productionLine',
  mixins: [d2CrudPlus.crud],
  data () {
    return {
      factoryInfo: []
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
      console.log('api', api)
      return api.createObj(row)
    },
    updateRequest (row) {
      console.log('----', row)
      return api.UpdateObj(row)
    },
    delRequest (row) {
      return api.DelObj(row.id)
    },
    // 获取生产工厂
    getFactory () {
      request({
        url: '/api/basics_manage/factory_info/',
        method: 'get',
        params: { status: 1 }
      }).then(res => {
        const { data } = res.data
        this.factoryInfo = data
      })
    },
    // form打开事件
    handleDialogOpened ({ mode, form, template, groupTemplate }) {
      if (mode === 'add') {
        if (this.factoryInfo.length === 1) {
          template.belong_to_factory.component.disabled = true
          form.belong_to_factory = this.factoryInfo[0].id
          if (!form.code && !form.code) {
            form.code = util.autoShortCreateCode()
          }
        }
      }
    }
  },
  mounted () {
    this.getFactory()
  }
}
</script>
