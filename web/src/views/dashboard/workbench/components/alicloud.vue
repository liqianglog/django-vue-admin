<template>
  <el-card shadow="never" header="阿里云" class="item-background">
    <img src="/image/card/ali.png" @click="Jump()" alt="阿里云" class="img-style">
  </el-card>
</template>

<script>
export default {
  title: '阿里云推广',
  icon: 'el-icon-present',
  description: '阿里云推广',
  height: 15,
  minH: 10,
  width: 14,
  minW: 10,
  isResizable: true,
  methods: {
    Jump () {
      window.open('https://www.aliyun.com/minisite/goods?userCode=jpef8a71&share_source=copy_link', '_black')
    }
  }
}
</script>
