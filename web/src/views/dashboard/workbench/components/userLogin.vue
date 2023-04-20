<template>
  <el-card
    class="card-view"
    :style="{
      backgroundColor: randomColor(),
    }"
  >
    <!-- shadow="always" -->
    <div id="myChart" :style="{width: wpx+'px',height: hpx+'px'}"></div>
  </el-card>
</template>

<script>
import { request } from '@/api/service'
export default {
  sort: 6,
  title: '用户登录趋势',
  name: 'userLogin',
  icon: 'el-icon-s-data',
  description: '用户登陆',
  height: 28,
  width: 20,
  isResizable: true,
  props: {
    hpx: {
      type: Number
    },
    wpx: {
      type: Number
    }
  },
  data () {
    this.myChart = null
    return {
      time: [],
      radio: '7'

    }
  },
  methods: {
    initGet () {
      request({
        url: '/api/system/homepage_statistics/'
      }).then((res) => {
        this.time = res.data.sum_days_login_list
        console.log(2, this.time)
        this.drawLine(this.time)
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
      const xAxisData = this.time.map(item => item.time)
      const seriesData = this.time.map(item => item.count)

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
          data: ['用户登陆数'],
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
            interval: function (index, value) {
              // 控制 x 轴上的刻度标签每隔一定数量显示一次
              return index % 2 === 0
            }, // 强制显示所有刻度
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
            name: '用户登陆数',
            type: 'line',
            data: seriesData,
            symbol: 'circle',
            smooth: true,
            symbolSize: 6,
            lineStyle: {
              color: 'rgba(0, 128, 255, 0.8)',
              width: 2
            },
            itemStyle: {
              color: 'rgba(0, 128, 255, 0.8)',
              borderColor: 'rgba(0, 128, 255, 1)',
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
    this.myChart = this.$echarts.init(document.getElementById('myChart'))
    this.initGet()
    this.drawLine()
    console.log(111, this.wpx, this.hpx)
    this.myChart.resize({ width: this.wpx, height: this.hpx })
  }
}
</script>

  <style scoped lang="scss">
.card-view {
  //border-radius: 10px;
  color: #ffffff;
}
.el-card{
  height: 100%;
}
::v-deep .el-card__body {
  width: 100%;
  height: 100%;
}

.el-radio-button__inner {
  border-radius: 20px;
}
</style>
