<template>
  <el-card shadow="hover" header="关于项目" class="card-view" :style="{backgroundColor:randomColor()}">
    <p>基于RBAC模型的权限控制的一整套基础开发平台，前后端分离，后端采用 django+django-rest-framework，前端采用
      vue+ElementUI+d2-crud-plus。如果喜欢就点个星星支持一下。
      <a href='https://gitee.com/liqianglog/django-vue-admin'>
        <img src='https://gitee.com/liqianglog/django-vue-admin/badge/star.svg?theme=dark' alt='star'
             style="position: absolute;right: 20px;bottom: 10px;"/>
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
  minH: 10,
  minW: 2,
  isResizable: true,
  config: {
    color: {
      label: '背景颜色',
      type: 'color',
      value: '',
      placeholder: '颜色为空则随机变换颜色'
    }
  },
  props: {
    config: {
      type: Object,
      required: false
    }
  },
  data () {
    return {}
  },
  methods: {
    // 生成一个颜色
    randomColor () {
      if (this.config?.color?.value) {
        return this.config.color.value
      }
      return this.color || this.$util.randomColor()
    }
  }
}
</script>

<style scoped lang="scss">
.card-view {
  color: #FFFFFF;

  p {
    font-size: 0.7em;
    color: #FFFFFF;
  }
}
.el-card{
  height: 100%;
}
::v-deep .el-card__body {
  height: 110px;

}
</style>
