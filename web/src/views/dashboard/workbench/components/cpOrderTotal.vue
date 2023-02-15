<template>
  <el-card class="box-card">
    <div>
      <el-statistic group-separator="," :precision="0" :value="order_total" title="码包订单总数"></el-statistic>
    </div>
  </el-card>
</template>

<script>
export default {
  title: '码包订单总数',
  icon: 'el-icon-monitor',
  description: '码包订单总数',
  name: 'cpOrderTotal',
  data () {
    return {
      order_total:50
    }
  }
}
</script>

<style scoped>

</style>
