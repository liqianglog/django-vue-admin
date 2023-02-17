<template>
  <div>
    <el-progress :percentage="currentValue" :color="setColor" :format="format"></el-progress>
  </div>
</template>
<script>
// 行展示组件进阶版
// 本示例演示要对传入的值做一些改变，然后再展示
export default {
  name: 'table-progress',
  props: {
    // 接收row.xxx的值
    value: {
      type: String || Number,
      required: false
    }
  },
  data () {
    return {
      currentValue: ''
    }
  },
  watch: {
    value (value) {
      // this.$emit('change', value)
      if (this.currentValue === value) {
        return
      }
      this.setValue(value)
    }
  },
  created () {
    this.setValue(this.value)
  },
  methods: {
    setValue (value) {
      // 在这里对 传入的value值做处理
      this.currentValue = Number(this.value)
      // 根据值的key 递归获取对应的名称
    },
    setColor () {
      if (this.value <= 50) {
        return '#F56C6C'
      } else if (this.value > 50 && this.value < 80) {
        return '#E6A23C'
      } else {
        return '#67C23A'
      }
    },
    format (percentage) {
      return `${percentage}%`
    }
  }
}
</script>
