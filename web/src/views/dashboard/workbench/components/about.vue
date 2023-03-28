<template>
  <el-card  shadow="hover" header="关于项目" class="card-view" :style="{backgroundColor:randomColor()}">
    <p>后端:Django-rest-framework</p>
    <p>前端:Vue2 + Element-UI + d2-crud-plus</p>
    <p>快速系统开发平台，,如果喜欢就点个星星支持一下。</p>
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
  height: 10,
  width: 8,
  minH: 10,
  minW: 4,
  isResizable: true,
  data () {
    return {}
  },
  methods:{
    // 生成一个随机整数
    randomColor () {
      const color = [
        '#50A8F4FF',
        '#FD6165FF',
        '#E679D8FF',
        '#F9AB5BFF'
      ]
      const ran = Math.floor(Math.random() * 4)
      return color[ran]
    }
  }
}
</script>

<style scoped lang="scss">
.card-view{
  color: #FFFFFF;
p {
  font-size: 0.7em;
  color: #FFFFFF;
}
}
</style>
