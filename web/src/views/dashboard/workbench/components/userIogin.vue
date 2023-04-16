<template>
  <el-card
    class="card-view"
    :style="{
      backgroundColor: randomColor(),
    }"
  >
    <!-- shadow="always" -->
    <div id="myChart" style="width: 530px; height: 300px; left: -15px"></div>
  </el-card>
</template>
  
  <script>
import { request } from "@/api/service";
export default {
  title: "用户登录折线图",
  icon: "el-icon-s-data",
  description: "用户登陆",
  name: "user",
  height: 28,
    width: 10,
    minH: 10,
    minW: 4,
  isResizable: true,
  name: "eCharts",
  data() {
    this.myChart=null
    return {
      time:[]

    };
  },
  methods: {
    initGet () {
    request({
      url: '/api/system/homepage_statistics/'
    }).then((res)=>{
      this.time=res.data.sum_days_login_list
this.drawLine(this.time)
    })
  },
    // 生成一个随机整数
    randomColor() {
      const color = ["#fffff"];
      const ran = Math.floor(Math.random() * 4);
      return color[ran];
    },
    drawLine() {
      // 基于准备好的dom，初始化echarts实例
      // 绘制图表
    this. myChart.setOption({
        title: { text: "" },
        tooltip: {},
        xAxis: {
          data: this.time.map(item=>item.time),
          boundaryGap: false,
          axisLabel: {
            interval: 0, //强制显示所有刻度
            rotate: 6, 
          },
        },
        yAxis: {},
        legend: {
          data: ["用户登陆数"],
        },
        series: [
          {
            name: "用户登陆数",
            type: "line",
            data: this.time.map(item=>item.count),
            areaStyle: {},
            areaStyle: {
              //折线的颜色
              color: "rgb(116,135,206)",
            },
            itemStyle: {
              color: "rgb(67,89,185)", // 设置折线图为红色
            },
          },
        ],
      });
    },
  },
  mounted() {
   this. myChart =this.$echarts.init(document.getElementById("myChart"));
    this.initGet();
    this.drawLine();
  },
};
</script>
  
  <style scoped lang="scss">
.card-view {
  border-radius: 10px;
  color: #ffffff;
}
.el-card{
  height: 100%;
}
::v-deep .el-card__body {
  width: 470px;
  height: 300px;

}
</style>
  