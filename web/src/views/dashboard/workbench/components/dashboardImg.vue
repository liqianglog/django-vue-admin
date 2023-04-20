<template>
  <el-card shadow="never" class="item-background">
    <img :src="config.src.value || '/image/card/tencent.jpg'" @click="Jump()" class="img-style">
  </el-card>
</template>

<script>
export default {
  sort: 8,
  title: '宣传图',
  name: 'dashboardImg',
  icon: 'el-icon-medal',
  description: '用于展示各种图片宣传页',
  height: 10,
  width: 16,
  isResizable: true,
  config: {
    src: {
      label: '图片地址',
      type: 'input',
      value: '/image/card/tencent.jpg',
      placeholder: '请输入图片地址',
      rules: [{ required: true, message: '不能为空' }]
    },
    url: {
      label: '跳转地址',
      type: 'input',
      placeholder: '请输入跳转地址',
      value: 'https://cloud.tencent.com/act/cps/redirect?redirect=1060&cps_key=b302a514a6688aa30823fac954464e5d&from=console',
      rules: [{ required: true, message: '不能为空' }]
    }
  },
  props: {
    config: {
      type: Object,
      required: false
    }
  },
  data () {
    return {
    }
  },
  methods: {
    Jump () {
      window.open(this.config.url.value, '_black')
    }
  }
}
</script>

<style scoped lang="scss">
.img-style {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 4px;
  cursor: pointer;
}
.el-card{
  height: 100%;
}
::v-deep .el-card__body {
    padding: 0;
  border-radius: 4px;
}
</style>
