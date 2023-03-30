<template>
  <el-card shadow="never" header="腾讯云" class="item-background">
    <img src="/image/card/tencent.jpg" @click="Jump()" alt="腾讯云" class="img-style">
  </el-card>
</template>

<script>
export default {
  title: '腾讯云推广',
  icon: 'el-icon-medal',
  description: '腾讯云推广',
  height: 10,
  minH: 10,
  width: 5,
  isResizable: true,
  methods: {
    Jump () {
      window.open('https://cloud.tencent.com/act/cps/redirect?redirect=1060&cps_key=b302a514a6688aa30823fac954464e5d&from=console', '_black')
    }
  }
}
</script>

<style>
.img-style {
  cursor: pointer;
  height: 180px;
  display: block;
  margin: auto;
}
</style>
