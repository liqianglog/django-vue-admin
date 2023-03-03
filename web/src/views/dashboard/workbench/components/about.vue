<template>
  <el-card  shadow="hover" header="关于项目" class="item-background">
    <p>高性能 / 精致 / 优雅。基于Vue2 + Element-UI 的中后台前端解决方案，如果喜欢就点个星星支持一下。</p>
    <p>
      <a href='https://liqianglog.gitee.io/django-vue-admin' target="_blank">
        <img src='https://liqianglog.gitee.io/django-vue-admin/badge/star.svg?theme=dark' alt='star' style="vertical-align: middle">
      </a>
    </p>
  </el-card>
</template>

<script>
export default {
  title: '关于项目',
  icon: 'el-icon-setting',
  description: '点个星星支持一下',
  height: 20,
  width: 8,
  minH: 20,
  minW: 4,
  isResizable: true,
  data () {
    return {}
  }
}
</script>

<style scoped>
.item-background p {
  color: #999;
}
</style>
