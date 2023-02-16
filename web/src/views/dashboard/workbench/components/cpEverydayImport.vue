<template>
<el-card>
  <div ref="cpEverydayImportRef" style="width: 100%;height: 400px">
  </div>
</el-card>
</template>

<script>
import * as echarts from 'echarts'
export default {
  title: '每日码包导入数',
  icon: 'el-icon-monitor',
  description: '每日码包导入数',
  name: 'cpEverydayImport',
  height: 5,
  width: 8,
  maxH: 1,
  maxW: Infinity,
  isResizable: true,
  data () {
    return {
      myChart: null
    }
  },
  methods: {
    initLine () {
      const echarDemo = this.$refs.cpEverydayImportRef
      this.myChart = echarts.init(echarDemo)
      const option = {
        title: {
          text: '当月每日码包导入数量'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['校验成功数', '校验失败数']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '校验失败数',
            type: 'line',
            stack: 'Total',
            data: [120, 132, 101, 134, 90, 230, 210],
            symbolSize: 6,
            symbol: 'circle',
            smooth: true,
            lineStyle: { color: '#fe9a8b' },
            itemStyle: { color: '#fe9a8b', borderColor: '#fe9a8b' },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#fe9a8bb3' },
                { offset: 1, color: '#fe9a8b03' }
              ])
            }
          },
          {
            name: '校验成功数',
            type: 'line',
            stack: 'Total',
            data: [220, 182, 191, 234, 290, 330, 310],
            lineStyle: { color: '#9E87FF' },
            itemStyle: { color: '#9E87FF', borderColor: '#9E87FF' },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#9E87FFb3' },
                { offset: 1, color: '#9E87FF03' }
              ])
            }
          }
        ]
      }
      this.myChart.setOption(option)
    }
  },
  mounted () {
    this.initLine()
  }
}
</script>

<style scoped>

</style>
