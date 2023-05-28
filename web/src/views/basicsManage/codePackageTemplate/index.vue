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
  name: 'codePackageTemplate',
  mixins: [d2CrudPlus.crud],
  components: {
    attrFieldForm
  },
  data () {
    return {
      formData: {
        fieldList: [{
          number: 0,
          name: '',
          is_code_content: false,
          char_length: '',
          verify_matches: ''
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
    nestIdSelected (value, form) {
      this.$emit('selected', value)
      form.nestId = value.id
      this.currentNestName = value.name
    }
  }
}
</script>
