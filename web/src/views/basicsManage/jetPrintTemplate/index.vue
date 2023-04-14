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
      <template slot="attr_fieldsFormSlot" slot-scope="scope">
       <attrFieldForm ref="attrFieldFormRef" :formData="formData" :scope="scope" ></attrFieldForm>
      </template>
    </d2-crud-x>
  </d2-container>
</template>

<script>
import * as api from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
import { BUTTON_WHETHER_BOOL } from '@/config/button'
import attrFieldForm from './components/attrFieldForm.vue'
export default {
  name: 'jetPrintTemplate',
  mixins: [d2CrudPlus.crud],
  components: {
    attrFieldForm
  },
  data () {
    return {
      formData: {
        fieldList: [{
          number: 1,
          name: '',
          line_number: 0,
          column_number: 0
        }]
      }
    }
  },
  methods: {
    BUTTON_WHETHER_BOOL () {
      return BUTTON_WHETHER_BOOL
    },
    getCrudOptions () {
      return crudOptions(this)
    },
    pageRequest (query) {
      return api.GetList(query)
    },
    addRequest (row) {
      const fields = this.$refs.attrFieldFormRef.submitForm()
      if (fields) {
        row.attr_fields = fields
        row.fields = fields.length
        return api.createObj(row)
      } else {
        return false
      }
    },
    updateRequest (row) {
      const fields = this.$refs.attrFieldFormRef.submitForm()
      console.log(fields)
      if (fields) {
        row.attr_fields = fields
        row.fields = fields.length
        return api.UpdateObj(row)
      } else {
        return false
      }

    },
    delRequest (row) {
      return api.DelObj(row.id)
    },
    // 监听表单打开事件,给自定义字段赋值
    handleDialogOpened ({ mode, form, template, groupTemplate }) {
      if(mode==='add') {
        this.formData = {
          fieldList: [{
            number: 1,
            name: '',
            line_number: 0,
            column_number: 0
          }]
        }
      }
      if (mode === 'edit' || mode === 'view') {
        const { attr_fields } = form
        this.formData.fieldList = attr_fields
      }
    }
  }
}
</script>
