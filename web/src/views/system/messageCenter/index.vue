<template>
  <d2-container :class="{'page-compact':crud.pageOptions.compact}">

    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @form-component-ready="handleFormComponentReady"
    >
      <div slot="header">
        <crud-search ref="search" :options="crud.searchOptions" @submit="handleSearch"  />
        <el-button size="small" type="primary" @click="addRow"><i class="el-icon-plus"/> 新增</el-button>
        <el-tabs v-model="tabActivted" @tab-click="onTabClick">
          <el-tab-pane label="我的发布" name="send"></el-tab-pane>
          <el-tab-pane label="我的接收" name="receive"></el-tab-pane>
        </el-tabs>
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
import { AddObj, GetObj, GetList, UpdateObj, DelObj, GetSelfReceive } from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
export default {
  name: 'messageCenter',
  components: {},
  mixins: [d2CrudPlus.crud],
  data () {
    return {
      tabActivted: 'send'
    }
  },
  created () {
    // 配置编辑前获取详情
    this.crud.options.fetchDetail = this.fetchDetail
  },
  computed: {
  },
  methods: {
    getCrudOptions () {
      return crudOptions(this)
    },
    pageRequest (query) {
      if (this.tabActivted === 'receive') {
        return GetSelfReceive({ ...query })
      }
      return GetList(query)
    },
    infoRequest (query) {
      return GetObj(query)
    },
    addRequest (row) {
      return AddObj(row).then(res => {
        const message = {
          message_id: res.data.id,
          contentType: 'TEXT',
          content: '您有新的消息,请到消息中心查看~'
        }
        this.$websocket.webSocketSend(message)
      })
    },
    updateRequest (row) {
      return UpdateObj(row)
    },
    delRequest (row) {
      return DelObj(row.id)
    },
    // 编辑对话框打开前获取详情
    fetchDetail (index, row) {
      if (index == null) {
        // 添加
        return {}
      }
      return GetObj(row).then(res => {
        return res.data
      })
    },
    handleFormComponentReady (event, key, form) {
      // console.log('form component ready:', event, key, form)
    },
    onTabClick (obj) {
      this.doRefresh()
    }
  }
}
</script>
