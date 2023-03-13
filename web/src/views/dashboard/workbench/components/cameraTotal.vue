<template>
  <el-card class="box-card">
    <div>
      <el-statistic group-separator="," :precision="0" :value="camera_total" title="相机数量"></el-statistic>
    </div>
  </el-card>
</template>

<script>
import { request } from '@/api/service'

export default {
  title: '相机数量',
  icon: 'el-icon-monitor',
  description: '相机数量',
  name: 'cameraTotal',
  height: 6,
  width: 4,
  minH: 6,
  minW: 4,
  isResizable: true,
  data () {
    return {
      camera_total: 50
    }
  },
  methods: {
    initGet () {
      request({
        url: '/api/datav/index/number_info/'
      }).then(res => {
        const { data } = res
        this.camera_total = data.camera_total
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
