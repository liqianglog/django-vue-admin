<template>
  <div>
    <el-row>
      <el-col :span="4">
        <div style="text-align: center">字段名</div>
      </el-col>
      <el-col :span="6">
        <div style="text-align: center">字段值</div>
      </el-col>
    </el-row>
    <el-form :model="currentForm" ref="currentFormRef" label-width="0px" size="mini">
      <el-row style="margin-bottom: 20px" :gutter="10" v-for="(field, index) in currentForm.attribute_fields" :key="index">
        <el-col :span="4">
         <div style="text-align: center;line-height: 2em">{{field.label}}</div>
        </el-col>
        <el-col :span="6">
          <el-form-item
            :prop="'attribute_fields.' + index + '.value'"
            :rules="[
                { required: field.required, message: '不能为空', trigger: 'blur' },
              ]"
          >
            <el-input v-model="field.value" :disabled="scope.mode==='view'" placeholder="请输入字段值"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>

<script>
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
          attribute_fields: [{
            label: '',
            required: false,
            value: ''
          }]

        }
      }
    }
  },
  computed: {
    currentForm () {
      return this.formData
    }
  },
  data () {
    return {}
  },
  methods: {
    submitForm () {
      let res =""
      this.$refs.currentFormRef.validate((valid) => {
        if (valid) {
          // alert('submit!')
          const { attribute_fields } = this.currentForm
          res = attribute_fields
          // return true
        } else {
          console.log('error submit!!')
          return false
        }
      })
      return res
    }
  }
}
</script>

<style scoped>

</style>
