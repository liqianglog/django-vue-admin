<template>
  <el-card
    class="card-view"
    :style="{
      backgroundColor: randomColor(),
    }"
  >
    <div id="main" :style="{width: pxData.wpx+'px',height: pxData.hpx+'px'}"></div>
  </el-card>
</template>

<script>
import { request } from '@/api/service'

export default {
  sort: 7,
  title: '注册用户趋势',
  name: 'registeredUser',
  icon: 'el-icon-s-data',
  description: '用户注册',
  height: 28,
  width: 20,
  isResizable: true,
  props: {
    pxData: {
      type: Object,
      require: false,
      default: () => ({
        wpx: 0,
        hpx: 0
      })
    }
  },
  watch: {
    pxData: {
      handler () {
        // eslint-disable-next-line no-unused-expressions
        this.myChart?.resize({ width: this.pxData.wpx, height: this.pxData.hpx })
      },
      immediate: true,
      deep: true
    }
  },
  data () {
    this.myChart = null
    return {
      data: []
    }
  },
  methods: {
    initGet () {
      request({
        url: '/api/system/datav/registered_user/'
      }).then((res) => {
        this.data = res.data.registered_user_list
        this.drawLine(this.data)
      })
    },
    // 生成一个随机整数
    randomColor () {
      const color = ['#fffff']
      const ran = Math.floor(Math.random() * 4)
      return color[ran]
    },
    drawLine () {
      // 基于准备好的dom，初始化echarts实例
      // 绘制图表
      const xAxisData = this.data.map(item => item.day)
      const seriesData = this.data.map(item => item.count)
      const option = {
        tooltip: {
          trigger: 'axis',
          backgroundColor: 'rgba(255, 255, 255, 0.8)',
          textStyle: {
            color: '#666'
          },
          axisPointer: {
            lineStyle: {
              color: '#999',
              type: 'dotted',
              width: 1
            }
          },
          formatter: params => {
            const param = params[0]
            return `<div style="padding: 8px;"><div style="color: #333;">${param.name}</div><div style="color: #FFA500;">${param.value} 人</div></div>`
          }
        },
        legend: {
          data: ['用户注册数'],
          textStyle: {
            color: '#666',
            fontSize: 12
          }
        },
        grid: {
          top: 40,
          left: 40,
          right: 65,
          bottom: 60
        },
        xAxis: {
          data: xAxisData,
          boundaryGap: false,
          axisLine: {
            lineStyle: {
              color: '#aaa',
              width: 1
            }
          },
          axisLabel: {
            interval: 'auto',
            maxInterval: 1,
            rotate: 0,
            textStyle: {
              color: '#333',
              fontSize: 12
            }
          }
        },
        yAxis: {
          axisLine: {
            lineStyle: {
              color: '#aaa',
              width: 1
            }
          },
          axisLabel: {
            textStyle: {
              color: '#333',
              fontSize: 12
            }
          },
          splitLine: {
            lineStyle: {
              color: '#ddd',
              type: 'dotted',
              width: 1
            }
          }
        },
        series: [
          {
            name: '用户注册数',
            type: 'line',
            data: seriesData,
            symbol: 'circle',
            symbolSize: 6,
            smooth: true,
            lineStyle: {
              color: 'rgba(38,204,164, 0.8)',
              width: 2
            },
            itemStyle: {
              color: 'rgba(98,206,178, 0.8)',
              borderColor: 'rgba(38,204,164, 1)',
              borderWidth: 1
            },
            areaStyle: {
              color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  {
                    offset: 0,
                    color: 'rgba(140,189,250, 0.8)'
                  },
                  {
                    offset: 1,
                    color: 'rgba(0, 128, 255, 0)'
                  }
                ]
              }
            }
          }
        ]
      }
      this.myChart.setOption(option)
    }
  },
  mounted () {
    this.myChart = this.$echarts.init(document.getElementById('main'))
    this.initGet()
    this.drawLine()
  }
}
</script>

<style scoped lang="scss">
.card-view {
  //border-radius: 10px;
  color: $color-primary;
}

.el-card {
  height: 100%;
}
</style>
