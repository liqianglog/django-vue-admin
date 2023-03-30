<template>
  <el-card shadow="never" header="短信服务" class="item-background">
    <img src="/image/card/sms.png" @click="Jump()" alt="短信服务" class="img-style">
  </el-card>
</template>

<script>
export default {
  title: '短信服务',
  icon: 'el-icon-message',
  description: '点击跳转到短信服务',
  height: 10,
  minH: 10,
  width: 5,
  minW: 5,
  isResizable: true,
  methods: {
    Jump () {
      window.open('https://bbs.django-vue-admin.com/plugMarket/128.html', '_black')
    }
  }
}
</script>
