<template>
<el-card>
  <div  ref="verInfoPieRef" style="width: 100%;height: 400px">
  </div>
</el-card>
</template>

<script>
import * as echarts from 'echarts'
import { EleResize } from '@/plugin/resize'
import { request } from '@/api/service'
export default {
  title: '问题码占比情况',
  icon: 'el-icon-monitor',
  description: '问题码占比情况',
  name: 'verInfoPie',
  height: 45,
  width: 8,
  minH: 40,
  minW: 8,
  isResizable: true,
  data () {
    return {
      myChart: null
    }
  },
  methods: {
    initLine () {
      const echarDemo = this.$refs.verInfoPieRef
      this.myChart = echarts.init(echarDemo)
      EleResize.on(echarDemo, () => {
        this.myChart.resize()
      })
      request({
        url: '/api/datav/index/verify_code_pie/'
      }).then(res => {
        const { data } = res
        const option = {
          title: {
            text: '问题码占比情况',
            x: 'left',
            textStyle: { fontSize: '15', color: '#303133' }
          },
          tooltip: { trigger: 'item', formatter: '{b} <br/> {c}个' },
          legend: {
            type: 'scroll',
            orient: 'vertical',
            right: '0%',
            left: '65%',
            top: '0%',
            itemWidth: 14,
            itemHeight: 14,
            data: data.name_list,
            textStyle: {
              rich: {
                name: {
                  fontSize: 14,
                  fontWeight: 400,
                  width: 200,
                  height: 35,
                  padding: [0, 0, 0, 60],
                  color: '#303133'
                },
                rate: {
                  fontSize: 15,
                  fontWeight: 500,
                  height: 35,
                  width: 40,
                  padding: [0, 0, 0, 30],
                  color: '#303133'
                }
              }
            }
          },
          series: [
            {
              name: '重码数',
              type: 'pie',
              radius: ['82', '102'],
              avoidLabelOverlap: false,
              label: {
                show: false,
                position: 'center'
              },
              emphasis: {
                label: {
                  show: true,
                  fontSize: 40,
                  fontWeight: 'bold'
                }
              },
              labelLine: {
                show: false
              },
              data: data.data
            }
          ]
        }
        this.myChart.setOption(option)
      })
    }
  },
  mounted () {
    this.initLine()
    const echarDemo = this.$refs.verInfoPieRef
    this.$nextTick(()=>{
      EleResize.on(echarDemo, () => {
        this.myChart.resize()
      })
    })

  }
}
</script>

<style scoped>

</style>
