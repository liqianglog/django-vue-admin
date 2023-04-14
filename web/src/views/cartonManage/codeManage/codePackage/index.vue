<template>
  <d2-container :class="{'page-compact':crud.pageOptions.compact}">
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
      @onOrderLog="onOrderLog"
      @onImportLog="onImportLog"
    >
      <div slot="header">
        <el-tabs v-model="activeName" @tab-click="handleClick">
          <el-tab-pane label="全部" name="0"></el-tab-pane>
          <el-tab-pane label="校验成功" name="4"></el-tab-pane>
          <el-tab-pane label="校验失败" name="3"></el-tab-pane>
          <el-tab-pane label="待校验" name="1"></el-tab-pane>
          <el-tab-pane label="校验中" name="2"></el-tab-pane>
        </el-tabs>
        <crud-search ref="search" :options="crud.searchOptions" @submit="handleSearch"/>
        <el-button-group>
          <el-button size="small" type="primary" v-permission="'Create'" @click="addRow"><i class="el-icon-plus"/> 新增
          </el-button>
        </el-button-group>
        <crud-toolbar :search.sync="crud.searchOptions.show"
                      :compact.sync="crud.pageOptions.compact"
                      :columns="crud.columns"
                      @refresh="doRefresh()"
                      @columns-filter-changed="handleColumnsFilterChanged"/>
      </div>
<!--      其他字段属性-->
      <template slot="attribute_fieldsFormSlot" slot-scope="scope">
        <attrFieldForm ref="attrFieldFormRef" :formData="formData" :scope="scope"></attrFieldForm>
      </template>
    </d2-crud-x>
    <orderLog ref="orderLog" :options="selectRow"></orderLog>
    <importLog ref="importLog"></importLog>
  </d2-container>
</template>

<script>
import * as api from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
import orderLog from './component/orderLog'
import importLog from './component/importLog'
import attrFieldForm from './component/attrFieldForm'
import { request } from '@/api/service'
export default {
  name: 'codePackage',
  mixins: [d2CrudPlus.crud],
  components: {
    orderLog,
    importLog,
    attrFieldForm
  },
  data () {
    return {
      is_encrypted: false,
      selectRow: {},
      activeName: '0',
      isAttrShow: false,
      formData: {
        attribute_fields: [{
          label: '',
          required: false,
          value: ''
        }]

      }
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
      if (this.activeName !== '0') {
        query.validate_status = this.activeName
      }
      return api.GetList(query)
    },
    addRequest (row) {
      const fields = this.$refs.attrFieldFormRef.submitForm()
      if (fields) {
        row.attribute_fields = fields
        return api.AddObj(row)
      } else {
        return false
      }

    },
    updateRequest (row) {
      return api.UpdateObj(row)
    },
    delRequest (row) {
      return api.DelObj(row.id)
    },
    // 导入日志
    onOrderLog ({ row }) {
      this.$refs.orderLog.options = row
      this.$refs.orderLog.drawer = true
      this.$refs.orderLog.getInit()
    },
    // 导入报告
    onImportLog ({ row }) {
      this.$refs.importLog.options = row
      this.$refs.importLog.drawer = true
      this.$refs.importLog.getInit()
    },
    // 获取客户信息的其他属性值
    getCusomerInfoAttr (id) {
      request(
        {
          url: `/api/basics_manage/customer_info/${id}/get_attr_json/`,
          method: 'get'
        }
      ).then(res => {
        const { attribute_fields } = res.data
        this.formData.attribute_fields = attribute_fields
      })
    }
  }
}
</script>
