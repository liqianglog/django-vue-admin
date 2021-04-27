<template>
  <div class="instrument-board">
    <div v-if="showTopTitle && haveMultipleData" class="instrument-board-title">
      <el-select :value="topTitle"
                 @change="chooseDisplayInstrumentBoardData"
      >
        <el-option
          v-for="(item,index) in instrumentBoardData"
          :key="index"
          :label="item.name || item['dir_name']"
          :value="index"
        >
        </el-option>
      </el-select>

    </div>
    <div v-else-if="showTopTitle" class="instrument-board-title">
      {{ topTitle }}
    </div>

    <div :id="ringGraphId" class="instrument-board-body"></div>
    <div v-if="showSubTitle"
         class="instrument-board-subtitle"
         :title="subTitle.title"
    >{{ subTitle.content }}
    </div>
  </div>
</template>

<script>
import VueTypes from 'vue-types'
// 引入基本模板,按需加载
const echarts = require('echarts/lib/echarts')
require('echarts/lib/chart/gauge')

// 仪表盘颜色范围
const NORMAL_COLOR = {
  color: '#28BCFE',
  itemColor: ['#25bfff', '#5284de', '#2a95f9']
}
const WARNING_COLOR = {
  color: '#e6a23c',
  itemColor: ['#e6a23c', '#cc8b1d', '#ffaf18']
}
const DANGER_COLOR = {
  color: '#F56C6C',
  itemColor: ['#fd666d', '#cf1717', '#b31212']
}

export default {
  name: 'InstrumentBoard',
  props: {
    // 组件key
    ringGraphKey: VueTypes.string.isRequired,
    // 上标题
    showTopTitle: VueTypes.bool.def(false),
    // 下标题
    showSubTitle: VueTypes.bool.def(false),
    // top title 配置映射
    topTitleKeyToNameMapping: VueTypes.object.def({
      cpu: 'CPU使用率',
      memory: '内存使用率'
    }),
    instrumentBoardData: VueTypes.any.isRequired
  },
  data() {
    return {
      // 当前显示的数据
      currentInstrumentBoardData: {}
    }
  },
  computed: {
    // 仪表盘是否存在多个数据
    haveMultipleData() {
      return this.instrumentBoardData instanceof Array && this.instrumentBoardData.length > 0
    },
    // 使用率
    ringRate() {
      let ringRate = this.currentInstrumentBoardData.rate
      ringRate = ringRate < 1 ? ringRate * 100 : ringRate
      return parseFloat(ringRate.toFixed(4))
    },
    // 仪表盘id
    ringGraphId() {
      return `${this.ringGraphKey}UsingRate`
    },
    // 上方标题
    topTitle() {
      return this.currentInstrumentBoardData['dir_name'] || this.topTitleKeyToNameMapping[this.ringGraphKey] || this.ringGraphKey
    },
    // 下方标题
    subTitle() {
      let used = this.currentInstrumentBoardData['used'] ? this.currentInstrumentBoardData['used'] + '/' : ''
      let total = this.currentInstrumentBoardData['total'] ? this.currentInstrumentBoardData['total'] : ''
      let unit = this.currentInstrumentBoardData['unit'] ? ` (${this.currentInstrumentBoardData['unit']})` : ''
      let content = `${used}${total}${unit} `
      let title = (this.currentInstrumentBoardData['used'] ? '已用/' : '') + '总量(单位)'
      return { content, title }
    },
    // 使用率样式配置
    usingRateStyle() {
      return {
        fontSize: 18,
        ...this.getCircleColor(this.ringRate)
      }
    }
  },
  mounted() {
    if (this.haveMultipleData) {
      this.currentInstrumentBoardData = this.instrumentBoardData[0]
    } else {
      this.currentInstrumentBoardData = this.instrumentBoardData
    }
    this.drawBar()
  },
  methods: {
    drawBar() {
      let currentRate = [this.ringRate]
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
    },
    // 仪表盘样式-颜色
    getCircleColor(usingRate) {
      if (usingRate < 60) {
        return NORMAL_COLOR
      } else if (usingRate > 60 && usingRate < 80) {
        return WARNING_COLOR
      } else if (usingRate > 80) {
        return DANGER_COLOR
      }
      return NORMAL_COLOR
    },
    chooseDisplayInstrumentBoardData(index) {
      this.currentInstrumentBoardData = this.instrumentBoardData[index]
      this.drawBar()
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
