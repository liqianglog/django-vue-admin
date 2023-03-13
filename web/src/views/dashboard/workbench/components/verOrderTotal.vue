<template>
  <el-card class="box-card">
    <div>
      <el-statistic group-separator="," :precision="0" :value="verify_work_order_total" title="检测工单数"></el-statistic>
    </div>
  </el-card>
</template>

<script>
import { request } from '@/api/service'

export default {
  title: '检测工单数',
  icon: 'el-icon-monitor',
  description: '检测工单数',
  name: 'verOrderTotal',
  height: 6,
  width: 4,
  minH: 6,
  minW: 4,
  isResizable: true,
  data () {
    return {
      verify_work_order_total: 50
    }
  },
  methods: {
    initGet () {
      request({
        url: '/api/datav/index/number_info/'
      }).then(res => {
        const { data } = res
        this.verify_work_order_total = data.verify_work_order_total
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
