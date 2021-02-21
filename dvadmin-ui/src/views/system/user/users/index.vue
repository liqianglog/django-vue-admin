<template>
  <div>
    <el-row :gutter="15">
      <el-form ref="elForm" :model="formData" :rules="rules" size="medium" label-width="100px">
        <el-col :span="24">
          <el-form-item label="手机号" prop="mobile">
            <el-input v-model="formData.mobile" placeholder="请输入手机号" :maxlength="11" show-word-limit clearable
                      prefix-icon='el-icon-mobile' :style="{width: '100%'}"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="24">
          <el-form-item label="多行文本" prop="field101">
            <el-input v-model="formData.field101" type="textarea" placeholder="请输入多行文本"
                      :autosize="{minRows: 4, maxRows: 4}" :style="{width: '100%'}"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="24">
          <el-form-item label="滑块" prop="field102" required>
            <el-slider :max='100' :step='1' v-model="formData.field102"></el-slider>
          </el-form-item>
        </el-col>
        <el-col :span="24">
          <el-form-item label="时间范围" prop="field103">
            <el-time-picker v-model="formData.field103" is-range format="HH:mm:ss" value-format="HH:mm:ss"
                            :style="{width: '100%'}" start-placeholder="开始时间" end-placeholder="结束时间" range-separator="至"
                            clearable></el-time-picker>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-row gutter="15">
            <el-col :span="12">
              <el-form-item label="评分" prop="field105">
                <el-rate v-model="formData.field105"></el-rate>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="颜色选择" prop="field106" required>
                <el-color-picker v-model="formData.field106" size="medium"></el-color-picker>
              </el-form-item>
            </el-col>
          </el-row>
        </el-col>
        <el-col :span="24">
          <el-form-item size="large">
            <el-button type="primary" @click="submitForm">提交</el-button>
            <el-button @click="resetForm">重置</el-button>
          </el-form-item>
        </el-col>
      </el-form>
    </el-row>
  </div>
</template>
<script>
  export default {
    components: {},
    props: [],
    data() {
      return {
        formData: {
          mobile: '',
          field101: undefined,
          field102: 0,
          field103: null,
          field105: 0,
          field106: null,
        },
        rules: {
          mobile: [{
            required: true,
            message: '请输入手机号',
            trigger: 'blur'
          }, {
            pattern: /^1(3|4|5|7|8|9)\d{9}$/,
            message: '手机号格式错误',
            trigger: 'blur'
          }],
          field101: [{
            required: true,
            message: '请输入多行文本',
            trigger: 'blur'
          }],
          field103: [{
            required: true,
            message: '时间范围不能为空',
            trigger: 'change'
          }],
          field105: [{
            required: true,
            message: '评分不能为空',
            trigger: 'change'
          }],
        },
      }
    },
    computed: {},
    watch: {},
    created() {},
    mounted() {},
    methods: {
      submitForm() {
        this.$refs['elForm'].validate(valid => {
          if (!valid) return
          // TODO 提交表单
        })
      },
      resetForm() {
        this.$refs['elForm'].resetFields()
      },
    }
  }

</script>
<style>
  .el-rate {
    display: inline-block;
    vertical-align: text-top;
  }

</style>
