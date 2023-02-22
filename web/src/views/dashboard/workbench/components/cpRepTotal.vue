<template>
  <el-card class="box-card">
    <div>
      <el-statistic group-separator="," :precision="0" :value="codepackage_repetition_total" title="码包重码总数"></el-statistic>
    </div>
  </el-card>
</template>

<script>
import { request } from '@/api/service'

export default {
  title: '码包重码总数',
  icon: 'el-icon-monitor',
  description: '码包重码总数',
  name: 'cpRepTotal',
  height: 6,
  width: 4,
  minH: 6,
  minW: 8,
  isResizable: true,
  data () {
    return {
      codepackage_repetition_total: 50
    }
  },
  methods: {
    initGet () {
      request({
        url: '/api/datav/index/number_info/'
      }).then(res => {
        const { data } = res
        this.codepackage_repetition_total = data.codepackage_repetition_total
      })
    }
  },
  mounted () {
    this.initGet()
  }
}
</script>

<style scoped>

</style>
