<template>
  <el-card shadow="hover" class="card-view" :style="{backgroundColor:randomColor()}" header="版本信息">
    <div style="text-align: center;color: #FFFFFF">
      <h2 style="margin-top: 5px;">{{ title }}</h2>
      <p style="margin-top: 5px;">最新版本 {{ ver }}</p>
    </div>
  </el-card>
</template>

<script>
import { mapState } from 'vuex'

export default {
  title: '版本信息',
  icon: 'el-icon-monitor',
  description: '当前项目版本信息',
  height: 10,
  minH: 10,
  width: 8,
  minW: 4,
  isResizable: true,
  data () {
    return {
      ver: 'loading...',
      title: ''
    }
  },
  mounted () {
    this.getVer()
  },
  computed: {
    ...mapState('d2admin', {
      siteName: state => state.settings.data['login.site_name'] // 网站名称
    })
  },
  methods: {
    async getVer () {
      this.ver = `v${process.env.VUE_APP_VERSION}` || 'v2.1.1'
      this.title = this.siteName || process.env.VUE_APP_TITLE
    },
    golog () {
      window.open('https://gitee.com/liqianglog/django-vue-admin/releases')
    },
    gogit () {
      window.open('https://gitee.com/liqianglog/django-vue-admin')
    },
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
  //background: rgb(80,168,244);
  //box-shadow: 1px 6px 8px 2px rgba(80,168,244,0.2);
  .card-content{
    //text-align: center;
  }
}
</style>
