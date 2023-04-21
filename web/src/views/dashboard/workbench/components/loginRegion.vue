<template>
  <el-card
    class="card-view"
    :style="{
      backgroundColor: randomColor(),
    }"
  >
    <div id="region" :style="{width: pxData.wpx+'px',height: pxData.hpx+'px'}"></div>
  </el-card>
</template>

<script>
import { request } from '@/api/service'

export default {
  sort: 7,
  title: '登录区域分布',
  name: 'loginRegion',
  icon: 'el-icon-s-data',
  description: '登录区域分布详情',
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
        url: '/api/system/datav/login_region/'
      }).then((res) => {
        this.data = res.data
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
      const xAxisData = this.data.map(item => item.region)
      const seriesData = this.data.map(item => item.count)
      const option = {
        title: {
          text: '登录区域分布',
          textStyle: {
            color: '#666666',
            fontSize: 14,
            fontWeight: '600'
          },
          left: 'left'
        },
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
            return `<div style="padding: 8px;"><div style="color: #333;">${param.name}</div><div style="color: #FFA500;">${param.value} 次</div></div>`
          }
        },
        legend: {
          data: ['登录区域分布'],
          textStyle: {
            color: '#666',
            fontSize: 12
          }
        },
        grid: {
          top: 40,
          left: 40,
          right: 65,
          bottom: 75
        },
        xAxis: {
          data: xAxisData,
          boundaryGap: true,
          axisLine: {
            lineStyle: {
              color: '#aaa',
              width: 1
            }
          },
          axisLabel: {
            interval: '0',
            maxInterval: 1,
            rotate: 0,
            formatter: function (value) {
              return value.split('').join('\n')
            },
            textStyle: {
              color: '#333',
              fontSize: 10
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
            type: 'bar',
            data: seriesData,
            barWidth: 16,
            barGap: 0,
            barCategoryGap: '20%',
            itemStyle: {
              color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  {
                    offset: 0,
                    color: 'rgba(0, 128, 255, 1)'
                  },
                  {
                    offset: 1,
                    color: 'rgba(0, 128, 255, 0.2)'
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
    this.myChart = this.$echarts.init(document.getElementById('region'))
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
