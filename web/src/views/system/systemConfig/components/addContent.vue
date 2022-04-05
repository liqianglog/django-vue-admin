<template>
  <div style="padding: 20px">
    <el-form ref="form" :model="form" :rules="rules" label-width="80px">
      <el-form-item label="所属分组" prop="parent">
        <el-select v-model="form.parent" placeholder="请选择分组" clearable>
          <el-option :label="item.title" :value="item.id" :key="index"
                     v-for="(item,index) in parentOptions"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="标题" prop="title">
        <el-input v-model="form.title" placeholder="请输入" clearable></el-input>
      </el-form-item>
      <el-form-item label="key值" prop="key">
        <el-input v-model="form.key" placeholder="请输入" clearable></el-input>
      </el-form-item>
      <el-form-item label="表单类型" prop="form_item_type">
        <el-select v-model="form.form_item_type" placeholder="请选择" clearable>
          <el-option :label="item.label" :value="item.value" :key="index"
                     v-for="(item,index) in typeOptions"></el-option>
        </el-select>
      </el-form-item>
      <div v-if="[13,14].indexOf(form.form_item_type)>-1">
        <associationTable ref="associationTable" v-model="form.setting"
                          @updateVal="associationTableUpdate"></associationTable>
      </div>
      <el-form-item label="校验规则">
        <el-select v-model="form.rule" multiple placeholder="请选择(可多选)" clearable>
          <el-option :label="item.label" :value="item.value" :key="index"
                     v-for="(item,index) in ruleOptions"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="提示信息" prop="placeholder">
        <el-input v-model="form.placeholder" placeholder="请输入" clearable></el-input>
      </el-form-item>
      <el-form-item label="排序" prop="sort">
        <el-input-number v-model="form.sort" :min="0" :max="99"></el-input-number>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">立即创建</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import * as api from '../api'
import associationTable from './components/associationTable'

export default {
  name: 'addContent',
  inject: ['refreshView'],
  components: {
    associationTable
  },
  data () {
    return {
      form: {
        parent: null,
        title: null,
        key: null,
        form_item_type: null,
        rule: null,
        placeholder: null
      },
      rules: {
        parent: [
          {
            required: true,
            message: '请选择'
          }
        ],
        title: [
          {
            required: true,
            message: '请输入'
          }
        ],
        key: [
          {
            required: true,
            message: '请输入'
          },
          {
            pattern: /^[A-Za-z0-9]+$/,
            message: '只支持字母和数字的输入'
          }
        ],
        form_item_type: [
          {
            required: true,
            message: '请输入'
          }
        ]
      },
      // 父级内容
      parentOptions: [],
      // 表单类型
      typeOptions: [
        { value: 0, label: '短文本' },
        { value: 1, label: '长文本' },
        { value: 2, label: '数字框' },
        { value: 3, label: '选择框' },
        { value: 4, label: '单选框' },
        { value: 5, label: '复选框' },
        { value: 6, label: '日期' },
        { value: 7, label: '日期时间' },
        { value: 8, label: '时间' },
        { value: 9, label: '图片' },
        { value: 10, label: '文件' },
        { value: 11, label: '数组' },
        { value: 12, label: '关联表' },
        { value: 13, label: '关联表(多选)' }
      ],
      ruleOptions: [
        {
          label: '必填项',
          value: '{"required": true, "message": "必填项不能为空"}'
        },
        {
          label: '邮箱',
          value: '{ "type": "email", "message": "请输入正确的邮箱地址"}'
        }
      ]
    }
  },
  methods: {
    getParent () {
      api.GetList({
        parent__isnull: true,
        limit: 999
      }).then(res => {
        const { data } = res.data
        this.parentOptions = data
      })
    },
    // 提交
    onSubmit () {
      const that = this
      that.associationTableUpdate().then(() => {
        const form = JSON.parse(JSON.stringify(that.form))
        const rules = []
        for (const item of form.rule) {
          const strToObj = JSON.parse(item)
          rules.push(strToObj)
        }
        form.rule = rules
        that.$refs.form.validate((valid) => {
          if (valid) {
            api.createObj(form).then(res => {
              this.$message.success('新增成功')
              this.refreshView()
            })
          } else {
            console.log('error submit!!')
            return false
          }
        })
      })
    },
    // 关联表数据更新
    associationTableUpdate () {
      const that = this
      return new Promise(function (resolve, reject) {
        if (that.$refs.associationTable) {
          console.log(that.$refs.associationTable.onSubmit())
          if (!that.$refs.associationTable.onSubmit()) {
            // eslint-disable-next-line prefer-promise-reject-errors
            return reject(false)
          }
          const { formObj } = that.$refs.associationTable
          that.form.setting = formObj
          return resolve(true)
        } else {
          return resolve(true)
        }
      })
    }
  },
  created () {
    this.getParent()
  }
}
</script>

<style scoped>

</style>
