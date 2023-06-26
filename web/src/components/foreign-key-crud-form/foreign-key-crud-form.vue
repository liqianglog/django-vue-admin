<template>
  <div>
    <el-row>
      <el-col :span="elProps.index.span" v-if="elProps.index">
        <div style="text-align: center">{{ elProps.index.name }}</div>
      </el-col>
      <el-col :span="elProps.fields[key].span" v-for="(_, key) in elProps.fields" :key="key">
        <div style="text-align: center">{{ elProps.fields[key].name }}</div>
      </el-col>
      <el-col :span="2">
        <div style="text-align: center">操作</div>
      </el-col>
    </el-row>
    <el-form :model="currentForm" ref="currentFormRef" label-width="0px" size="mini" type="flex">
      <el-row style="margin-bottom: 0px" :gutter="5" v-for="(field, index) in currentForm.data" :key="index">
        <el-col :span="elProps.index.span" v-if="elProps.index">
          <div style="text-align: center">
            {{index+1}}
          </div>
        </el-col>
        <el-col :span="elProps.fields[key].span" v-for="(_,key) in elProps.fields" :key="key">
          <el-form-item
            :prop="'data.' + index + '.' + key"
            :rules="[
                { required: elProps.fields[key].required, message: '不能为空', trigger: 'blur' },
              ]"
          >
            <el-select v-model="field[key]" v-if="elProps.fields[key].type === 'select'" placeholder="请选择">
              <el-option
                v-for="item in elProps.fields[key].option"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
            <el-input-number style="width: 100%" v-else-if="elProps.fields[key].type === 'number'" controls-position="right" v-model="field[key]"></el-input-number>
            <el-input v-model="field[key]" v-else placeholder="请输入"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="4">
          <el-form-item>
          <el-button @click.prevent="topDomain(index)" :disabled="index === 0" type="primary" circle icon="el-icon-top"></el-button>
          <el-button @click.prevent="bottomDomain(index)" :disabled="index === currentForm.data.length - 1" type="primary" circle icon="el-icon-bottom"></el-button>
          <el-button @click.prevent="removeDomain(index)" type="danger" circle icon="el-icon-delete"></el-button>
          </el-form-item>
        </el-col>
      </el-row>
      <el-form-item>
        <el-col :span="12">
          <el-button type="primary" @click="addDomain">新增</el-button>
        </el-col>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
export default {
  name: 'foreignKeyCrudForm',
  model: {
    prop: 'value',
    event: ['change', 'input']
  },
  props: {
    elProps: {
      type: Object,
      default () {
        return {
          isInitRows: true, // 是否初始化一行
          index: {
            name: '序号',
            span: 2
          },
          fields: {
            description: {
              name: '内容描述',
              type: 'input',
              span: 10,
              default: null,
              required: true
            },
            content: {
              name: '类型',
              type: 'select',
              span: 4,
              default: 0,
              required: true,
              options: [{
                value: '0',
                label: '单选项'
              }, {
                value: '1',
                label: '多选项'
              }, {
                value: '2',
                label: '单行填空'
              }, {
                value: '3',
                label: '多行填空'
              }]
            },
            score: {
              name: '分数',
              type: 'number',
              span: 4,
              default: 0,
              required: true,
              min: 0,
              max: null
            }
          }
        }
      }
    },
    value: {
      type: Array,
      required: false
    }
  },
  data () {
    return {
    }
  },
  computed: {
    // eslint-disable-next-line vue/return-in-computed-property
    submitForm () {
      let res = ''
      this.$refs.currentFormRef.validate((valid) => {
        if (valid) {
          const { data } = this.currentForm
          res = data
        } else {
          console.log('error submit!!')
          return false
        }
      })
      return res
    },
    currentForm () {
      if (!this.value || !this.value[0]) {
        if (this.elProps.isInitRows) {
          const fields = {
            _id: this.value?.length || 0
          }
          for (const key in this.elProps.fields) {
            fields[key] = this.elProps.fields[key].default || null
          }
          this.$emit('change', [fields])
          this.$emit('input', [fields])
          return {
            data: [fields]
          }
        } else {
          return {
            data: []
          }
        }
      }
      return {
        data: this.value
      }
    }
  },
  created () {
  },
  methods: {
    // 数组元素互换位置，并且替换顺序
    swapArray (arr, index1, index2) {
      arr[index1] = arr.splice(index2, 1, arr[index1])[0]
      arr[index2].sort = index2 + 1
      arr[index1].sort = index1 + 1
      return arr
    },
    // 删除
    removeDomain (index) {
      this.currentForm.data.splice(index, 1)
      this.$emit('change', this.currentForm.data)
      this.$emit('input', this.currentForm.data)
    },
    // 上移
    topDomain (index) {
      this.swapArray(this.currentForm.data, index - 1, index)
      this.$emit('change', this.currentForm.data)
      this.$emit('input', this.currentForm.data)
    },
    // 下移
    bottomDomain (index) {
      this.swapArray(this.currentForm.data, index, index + 1)
      this.$emit('change', this.currentForm.data)
      this.$emit('input', this.currentForm.data)
    },
    // 新增
    addDomain () {
      const fields = {
        _id: this.value?.length || 0
      }
      for (const key in this.elProps.fields) {
        fields[key] = this.elProps.fields[key].default || null
      }
      fields.sort = (this.value?.length || 0) + 1
      this.currentForm.data.push(fields)
      this.$emit('change', this.currentForm.data)
      this.$emit('input', this.currentForm.data)
    }
  }
}
</script>
