<template>
<el-card>
  <div ref="pwoEverydayCreateRef" style="width: 100%;height: 400px">
  </div>
</el-card>
</template>

<script>
import * as echarts from 'echarts'
import { EleResize } from '@/plugin/resize'
import { request } from '@/api/service'
export default {
  title: '当月每日生产工单情况',
  icon: 'el-icon-monitor',
  description: '当月每日生产工单情况',
  name: 'pwoEveryday',
  height: 42,
  width: 12,
  minH: 42,
  minW: 12,
  isResizable: true,
  data () {
    return {
      myChart: null
    }
  },
  methods: {
    initLine () {
      const echarDemo = this.$refs.pwoEverydayCreateRef
      this.myChart = echarts.init(echarDemo)
      EleResize.on(echarDemo, () => {
        this.myChart.resize()
      })
      request({
        url: '/api/datav/index/production_work/'
      }).then(res => {
        const { data } = res
        const option = {
          title: {
            text: '当月每日生产工单情况'
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
            data: data.date_list
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              name: '新增数量',
              type: 'line',
              stack: 'Total',
              data: data.prod_number_list,
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
              name: '码包下载数',
              type: 'line',
              stack: 'Total',
              data: data.download_number_list,
              lineStyle: { color: '#9E87FF' },
              itemStyle: { color: '#9E87FF', borderColor: '#9E87FF' },
              areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#9E87FFb3' },
                  { offset: 1, color: '#9E87FF03' }
                ])
              }
            },
            {
              name: '生产前校验数',
              type: 'line',
              stack: 'Total',
              data: data.verify_number_list,
              lineStyle: { color: '#87e9ff' },
              itemStyle: { color: '#87e9ff', borderColor: '#9E87FF' },
              areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#87e9ffb3' },
                  { offset: 1, color: '#87e9ff03' }
                ])
              }
            }
          ]
        }
        this.myChart.setOption(option)
      })
    }
  },
  mounted () {
    this.initLine()
  }
}
</script>

<style scoped>

</style>
