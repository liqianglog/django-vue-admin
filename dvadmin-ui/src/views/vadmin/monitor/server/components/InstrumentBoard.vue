<template>
  <div class="instrument-board">
    <div v-if="topTitle.show" class="instrument-board-title">
      {{ topTitleKeyToNameMapping[topTitle.text] || topTitle.text }}
    </div>
    <div :id="ringGraphId" class="instrument-board-body"></div>
    <div v-if="subTitle.show" class="instrument-board-subtitle">{{ subTitleContent }}</div>
  </div>
</template>

<script>
import VueTypes from 'vue-types'
// 引入基本模板,按需加载
const echarts = require('echarts/lib/echarts')
require('echarts/lib/chart/gauge')

export default {
  name: 'InstrumentBoard',
  props: {
    // 组件唯一id
    ringGraphId: VueTypes.string.isRequired,
    // 上标题
    topTitle: VueTypes.shape({
      show: VueTypes.bool,
      text: VueTypes.string
    }).def({
      show: false
    }),
    // 下标题
    subTitle: VueTypes.shape({
      show: VueTypes.bool,
      total: VueTypes.any,
      used: VueTypes.any,
      unit: VueTypes.string
    }).def({
      show: false
    }),
    // 使用率-数值
    usingRate: VueTypes.number.isRequired,
    // 使用率样式配置
    usingRateStyle: VueTypes.object.def({
      color: '#28BCFE',
      fontSize: 18,
      itemColor: ['#25BFFF', '#5284DE', '#2A95F9']
    }),
    topTitleKeyToNameMapping: VueTypes.object.def({
      cpu: 'CPU使用率',
      memory: '内存使用率',
      disk: '磁盘使用率'
    })
  },
  data() {
    return {}
  },
  computed: {
    subTitleContent() {
      let used = this.subTitle.used ? this.subTitle.used + '/' : ''
      let total = this.subTitle.total ? this.subTitle.total : ''
      let unit = this.subTitle.unit ? ` (${this.subTitle.unit})` : ''
      return `${used}${total}${unit} `
    }
  },
  mounted() {
    this.drawBar()
  },
  methods: {
    drawBar() {
      let currentRate = [this.usingRate]
      // 基于dom，初始化echarts实例
      let RingGraph = echarts.init(document.getElementById(this.ringGraphId))

      let option = {
        title: {
          text: currentRate + '%',
          textStyle: this.usingRateStyle,
          itemGap: 10,
          left: 'center',
          top: '45%'
        },
        angleAxis: {
          max: 100,
          clockwise: true, // 逆时针
          // 隐藏刻度线
          show: false
        },
        radiusAxis: {
          type: 'category',
          show: true,
          axisLabel: {
            show: false
          },
          axisLine: {
            show: false
          },
          axisTick: {
            show: false
          }
        },
        polar: {
          center: ['50%', '50%'], // 坐标中心位置
          radius: '100%' //图形大小
        },
        series: [{
          type: 'bar',
          data: currentRate,
          showBackground: true,
          backgroundStyle: {
            color: '#BDEBFF' // 底圈颜色
          },
          coordinateSystem: 'polar',
          roundCap: true,
          barWidth: 15,
          itemStyle: {
            normal: {
              opacity: 1,
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                offset: 0,
                color: this.usingRateStyle.itemColor[0] || '#25BFFF'
              }, {
                offset: 1,
                color: this.usingRateStyle.itemColor[1] || '#5284DE'
              }]),
              shadowBlur: 1,
              shadowColor: this.usingRateStyle.itemColor[2] || '#2A95F9'
            }
          }
        }]
      }
      // 绘制图表
      RingGraph.setOption(option)
    }
  }
}
</script>

<style scoped>
.instrument-board-title {
  font-weight: bolder;
  text-align: center;
}

.instrument-board-body {
  min-height: 200px;
  min-width: 200px;
}

.instrument-board-subtitle {
  text-align: center;
}
</style>
