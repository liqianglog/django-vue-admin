<template>
    <el-card
      class="card-view"
      :style="{ backgroundColor: randomColor() }"
      shadow="always"
    >
      <div>
        <el-row type="flex" justify="space-around">
          <el-col :span="12">
            <div class="card-content-label">附件总数</div>
            <div class="card-content">
              <div class="card-content-value">{{ total || 0 }}</div>
              <div class="el-icon-document-copy">
                附件总数量</div>
            </div>
          </el-col>
          <el-col :span="12" :offset="6" style="text-align: right">
            <i class="real-time">实时</i>
            <div class="card-content-time">
              <div class="attachment-value">{{ total || 0 }}MB</div>
              <div class="el-icon-s-flag">
                占用空间</div>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </template>
  
  <script>
  import { request } from "@/api/service";
  
  export default {
    title: "附件总数统计图",
    icon: "el-icon-s-order",
    description: "附件总数量",
    name: "sumTotal",
    height: 14,
    width: 8,
    minH: 14,
    minW: 8,
    isResizable: true,
    data() {
      return {
        total: 0,
      };
    },
    methods: {
      initGet() {
        request({
          url: "",
        }).then((res) => {
          const { data } = res;
          // this.total = data.total;
        });
      },
      // 生成一个随机整数
      randomColor() {
        const color = ["#50A8F4FF", "#FD6165FF", "#E679D8FF", "#F9AB5BFF"];
        const ran = Math.floor(Math.random() * 4);
        return color[ran];
      },
    },
    mounted() {
      this.initGet();
    },
  };
  </script>
  
  <style scoped lang="scss">
  .card-view {
    border-radius: 10px;
    color: #ffffff;
    .card-content {
      .card-content-label {
        font-size: 0.8em;
        color: #ffffff;
      }
      .card-content-value {
        color: #ffffff;
        margin-top: 5px;
        font-size: 1.5em;
        font-weight: bold;
      }
    }
    .attachment-value {
      color: #ffffff;
      margin-top: 5px;
      font-size: 1.5em;
      font-weight: bold;
      margin-right: 180px;
    }
    .el-icon-document-copy {
      font-size: 12px;
    }
    .el-icon-s-flag {
      font-size: 12px;
      margin-right: 132px;
    }
  }
  .real-time {
    background: rgb(53, 59, 86);
    font-size: 14px;
    font-style: normal;
    padding: 0 7px 0 7px;
    border-radius: 4px;
  }
  </style>
  