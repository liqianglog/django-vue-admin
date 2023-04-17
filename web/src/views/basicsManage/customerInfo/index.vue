<template>
  <d2-container :class="{'page-compact':crud.pageOptions.compact}">
    <d2-crud-x
      ref="d2Crud"
      v-bind="_crudProps"
      v-on="_crudListeners"
    >
      <div slot="header">
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

      <template slot="attribute_fieldsFormSlot" slot-scope="scope">
        <el-row>
          <el-col :span="6">
            <div style="text-align: center">字段名</div>
          </el-col>
          <el-col :span="6">
            <div style="text-align: center">是否必填</div>
          </el-col>
          <el-col :span="2" v-show="scope.mode==='add'||scope.mode==='edit'">
            <div style="text-align: center">操作</div>
          </el-col>
        </el-row>
        <el-form :model="dynamicValidateForm" ref="dynamicValidateForm" label-width="0px" size="mini">
          <el-form-item
            v-for="(field, index) in dynamicValidateForm.attribute_fields"
            style="margin-bottom: 20px"
            :key="index"
            :prop="'attribute_fields.' + index + '.label'"
            :rules="{
      required: true, message: '不能为空', trigger: 'blur'
    }"
          >
            <el-col :span="6">
              <el-input v-model="field.label" :disabled="scope.mode==='view'" placeholder="请输入" clearable></el-input>
            </el-col>
            <el-col :span="6">
              <el-select v-model="field.required" :disabled="scope.mode==='view'" clearable>
                <el-option
                  v-for="item in BUTTON_WHETHER_BOOL()"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </el-col>
            <el-col :span="2" v-show="scope.mode==='add'||scope.mode==='edit'">
              <el-button  @click.prevent="removeDomain(field)">删除</el-button>
            </el-col>
          </el-form-item>
          <el-form-item>
            <el-col :span="6" v-show="scope.mode==='add'||scope.mode==='edit'">
              <el-button type="primary"  @click="addDomain">新增</el-button>
              <el-button @click="resetForm('dynamicValidateForm')" >重置</el-button>
            </el-col>
          </el-form-item>
        </el-form>
      </template>
    </d2-crud-x>
  </d2-container>
</template>

<script>
import * as api from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
import { BUTTON_WHETHER_BOOL } from '@/config/button'
import util from '@/libs/util'

export default {
  name: 'customerInfo',
  mixins: [d2CrudPlus.crud],
  data () {
    return {
      dynamicValidateForm: {
        attribute_fields: [{
          label: '',
          required: false,
          value: ''
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
      const bool = this.submitForm('dynamicValidateForm')
      if (bool) {
        const { attribute_fields } = this.dynamicValidateForm
        row.attribute_fields = attribute_fields
        return api.createObj(row)
      } else {
        return false
      }
      // return api.createObj(row)
    },
    updateRequest (row) {
      const bool = this.submitForm('dynamicValidateForm')
      if (bool) {
        const { attribute_fields } = this.dynamicValidateForm
        row.attribute_fields = attribute_fields
        return api.UpdateObj(row)
      } else {
        return false
      }
    },
    delRequest (row) {
      return api.DelObj(row.id)
    },
    // form相关
    submitForm (formName) {
      let bool = false
      // 判断this.dynamicValidateForm.attribute_fields是否长度大于0
      const { attribute_fields } = this.dynamicValidateForm
      if (attribute_fields.length === 1) {
        bool = true
      } else {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            // alert('submit!')
            bool = true
            return true
          } else {
            console.log('error submit!!')
          }
        })
      }

      return bool
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    },
    removeDomain (item) {
      var index = this.dynamicValidateForm.attribute_fields.indexOf(item)
      if (index !== -1) {
        this.dynamicValidateForm.attribute_fields.splice(index, 1)
      }
    },
    addDomain () {
      this.dynamicValidateForm.attribute_fields.push({
        label: '',
        required: false,
        value: ''
      })
    },
    // 监听表单打开事件,给自定义字段赋值
    handleDialogOpened ({ mode, form, template, groupTemplate }) {
      if (mode === 'add') {
        form.no = util.autoShortCreateCode()
      }
      if (mode === 'edit') {
        const { attribute_fields } = form
        this.dynamicValidateForm.attribute_fields = attribute_fields
      }
    }
  }
}
</script>
