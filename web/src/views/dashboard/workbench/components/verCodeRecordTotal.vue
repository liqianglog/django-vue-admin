<template>
  <el-card class="box-card">
    <div>
      <el-statistic group-separator="," :precision="0" :value="verify_code_record_total" title="检测问题码总数"></el-statistic>
    </div>
  </el-card>
</template>

<script>
import { request } from '@/api/service'

export default {
  title: '检测问题码总数',
  icon: 'el-icon-monitor',
  description: '检测问题码总数',
  name: 'verCodeRecordTotal',
  height: 6,
  width: 8,
  minH: 6,
  maxW: Infinity,
  isResizable: true,
  data () {
    return {
      verify_code_record_total: 50
    }
  },
  methods: {
    initGet () {
      request({
        url: '/api/datav/index/number_info/'
      }).then(res => {
        const { data } = res
        this.verify_code_record_total = data.verify_code_record_total
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
