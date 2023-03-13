<template>
  <el-card class="box-card">
    <div>
      <el-statistic group-separator="," :precision="0" :value="prod_work_total" title="生产工单数"></el-statistic>
    </div>
  </el-card>
</template>

<script>
import { request } from '@/api/service'

export default {
  title: '生产工单数',
  icon: 'el-icon-monitor',
  description: '生产工单数',
  name: 'pwoTotal',
  height: 6,
  width: 4,
  minH: 6,
  minW: 4,
  isResizable: true,
  data () {
    return {
      prod_work_total: 50
    }
  },
  methods: {
    initGet () {
      request({
        url: '/api/datav/index/number_info/'
      }).then(res => {
        const { data } = res
        this.prod_work_total = data.prod_work_total
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
