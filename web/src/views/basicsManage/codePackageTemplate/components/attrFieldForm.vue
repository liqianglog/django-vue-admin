<template>
  <div>
    <el-row>
      <el-col :span="4">
        <div style="text-align: center">字段序号</div>
      </el-col>
      <el-col :span="5">
        <div style="text-align: center">字段名称</div>
      </el-col>
      <el-col :span="4">
        <div style="text-align: center">字段长度</div>
      </el-col>
      <el-col :span="8">
        <div style="text-align: center">验证匹配符</div>
      </el-col>
      <el-col :span="2" v-show="scope.mode==='add'||scope.mode==='edit'">
        <div style="text-align: center">操作</div>
      </el-col>
    </el-row>
    <el-form :model="currentForm" ref="currentFormRef" label-width="0px" size="mini">
      <el-row style="margin-bottom: 0px" :gutter="10" v-for="(field, index) in currentForm.fieldList" :key="index">
        <el-col :span="4">
          <el-form-item  :prop="'fieldList.' + index + '.number'">
          <el-input-number style="width: 120px" controls-position="right" v-model="field.number" :disabled="scope.mode==='view'" :min="-1" :max="99"></el-input-number>
          </el-form-item>
        </el-col>
        <el-col :span="5">
          <el-form-item
            :prop="'fieldList.' + index + '.name'"
            :rules="[
                { required: true, message: '不能为空', trigger: 'blur' },
              ]"
          >
            <el-input v-model="field.name" :disabled="scope.mode==='view'" placeholder="请输入字段名称"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="4">
          <el-form-item
            :prop="'fieldList.' + index + '.char_length'"
            :rules="[
                { required: true, message: '不能为空', trigger: 'blur' }
              ]"
          >
            <el-input-number style="width: 120px" controls-position="right" v-model="field.char_length" :disabled="scope.mode==='view'" :min="-1" :max="99"></el-input-number>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item
            :prop="'fieldList.' + index + '.verify_matches'"
            :rules="[
                { required: false, message: '不能为空', trigger: 'blur' }
              ]"
          >
            <el-input v-model="field.verify_matches" :disabled="scope.mode==='view'" placeholder="请输入验证匹配符"
                      clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="2" v-show="scope.mode==='add'||scope.mode==='edit'">
          <el-form-item>
          <el-button @click.prevent="removeDomain(field)">删除</el-button>
          </el-form-item>
        </el-col>
      </el-row>
      <el-form-item>
<!--        <el-button type="primary" @click="submitForm('dynamicValidateForm')">提交</el-button>-->
        <el-col :span="6" v-show="scope.mode==='add'||scope.mode==='edit'">
          <el-button type="primary" @click="addDomain">新增</el-button>
          <el-button @click="resetForm('currentFormRef')">重置</el-button>
        </el-col>
      </el-form-item>
    </el-form>
    <div>
      <el-alert

        type="error">
        <div style="line-height: 1.5em">
          <template slot:title>
            <span style="font-size: 1.2em">说明</span>
          </template>
          <div>1.匹配符为字符中包含(或左匹配);</div>
          <div>2.根据字段属性,自动生成字段数;</div>
          <div> 3.字段长度-1时,不验证;</div>
          <div>4.匹配符为空,不验证;</div>
        </div>
        </el-alert>
    </div>
  </div>
</template>

<script>
import XEUtils from 'xe-utils'
export default {
  name: 'attrFieldForm',
  props: {
    scope: {
      type: Object
    },
    formData: {
      type: Object,
      default () {
        return {
          fieldList: [{
            number: 0,
            name: '',
            char_length: '',
            verify_matches: ''
          }]
        }
      }
    }
  },
  computed: {
    currentForm () {
      this.formData.fieldList = XEUtils.orderBy(this.formData.fieldList, 'number')
      return this.formData
    }
  },
  data () {
    return {}
  },
  methods: {
    submitForm () {
      let res = ''
      this.$refs.currentFormRef.validate((valid) => {
        if (valid) {
          // alert('submit!')
          const { fieldList } = this.currentForm
          res = fieldList
          // return true
        } else {
          console.log('error submit!!')
          return false
        }
      })
      return res
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    },
    removeDomain (item) {
      var index = this.currentForm.fieldList.indexOf(item)
      if (index !== -1) {
        this.currentForm.fieldList.splice(index, 1)
      }
    },
    addDomain () {
      let index = this.currentForm.fieldList.length
      if (this.scope.mode === 'edit') {
        index = index + 1
      }
      this.currentForm.fieldList.push({
        number: index,
        name: '',
        char_length: '',
        verify_matches: ''
      })
    }
  }
}
</script>

<style scoped>

</style>
