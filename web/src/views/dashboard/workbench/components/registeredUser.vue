<template>
    <el-card
      class="card-view"
      :style="{
        backgroundColor: randomColor(),
      }"
    >
      <div id="main" style="width: 530px; height: 300px; left: -18px"></div>
    </el-card>
  </template>
    
    <script>
  import { request } from "@/api/service";
  export default {
    title: "注册用户数折线图",
    icon: "el-icon-s-data",
    description: "用户注册",
    name: "registeredUser",
    height: 28,
    width: 10,
    minH: 10,
    minW: 4,
    isResizable: true,
    name: "eCharts",
    data() {
      return {};
    },
    methods: {
      initGet() {
        request({
          url: "",
        });
      },
      // 生成一个随机整数
      randomColor() {
        const color = ["#fffff"];
        const ran = Math.floor(Math.random() * 4);
        return color[ran];
      },
      drawLine() {
        // 基于准备好的dom，初始化echarts实例
        let myChart = this.$echarts.init(document.getElementById("main"));
        // 绘制图表
        myChart.setOption({
          title: { text: "" },
          tooltip: {},
          xAxis: {
            data: ["2023-4-8", "2023-4-9", "2023-4-10", "2023-4-11", "2023-4-12"],
            boundaryGap: false,
            axisLabel: {
              interval: 0, //强制显示所有刻度
            },
          },
          yAxis: {},
          legend: {
            data: ["注册用户数"],
          },
          series: [
            {
              name: "注册用户数",
              type: "line",
              data: [5, 20, 36, 10, 10, 20],
              //折线图的背景色
              areaStyle: {
                color: "rgb(98,206,178)",
              },
              //折线的颜色
              itemStyle: {
                color: "rgb(38,204,164)", // 设置折线图为红色
              },
            },
          ],
        });
      },
    },
    mounted() {
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
  </style>
    