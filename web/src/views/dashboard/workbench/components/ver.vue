<template>
  <el-card shadow="hover" header="版本信息">
    <div style="height: 70px;text-align: center;">
      <h2 style="margin-top: 5px;">Dvadmin</h2>
      <p style="margin-top: 5px;">最新版本 {{ ver }}</p>
    </div>
    <div style="margin-top: 5px;">
      <el-button type="primary" plain round @click="golog">更新日志</el-button>
      <el-button type="primary" plain round @click="gogit">gitee</el-button>
    </div>
  </el-card>
</template>

<script>
export default {
  title: '版本信息',
  icon: 'el-icon-monitor',
  description: '当前项目版本信息',
  height: 22,
  width: 8,
  minH: 22,
  minW: 4,
  isResizable: true,
  data () {
    return {
      ver: 'loading...'
    }
  },
  mounted () {
    this.getVer()
  },
  methods: {
    async getVer () {
      this.ver = 'v2.0.9'
    },
    golog () {
      window.open('https://gitee.com/liqianglog/django-vue-admin/releases')
    },
    gogit () {
      window.open('https://gitee.com/liqianglog/django-vue-admin')
    }
  }
}
</script>
