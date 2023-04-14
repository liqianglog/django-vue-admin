<template>
     <el-card class="card-view" :style= "{backgroundColor:randomColor()}" shadow="always"  >
      <div style="display:flex;flex: 1; flex-wrap: wrap;justify-content: space-between; margin-top: 10px;">
        <div style="flex: 1; min-width: 180px;max-width:180px;height: 80px; display: flex;">
            <el-col :span="4" class="lightgreen-box">
              <div class="underline">
              <i class="el-icon-s-promotion"></i>
            </div>
            </el-col>
            <el-col :span="20" class="orange-box">
              <div class="enroll-time">
                  <div class="enroll-number"><h3>{{total || 0}}</h3>
                  </div>
                  <div class="enroll-text">今日注册
                  </div>
                </div>
            </el-col>
          </div>
          <div style="flex: 1;min-width: 180px;max-width:180px;height: 80px; display: flex;">
            <el-col :span="4" class="lightgreen-box">
              <div class="underline">
              <i class="el-icon-chat-line-square"></i>
            </div>
            </el-col>
            <el-col :span="20" class="orange-box">
              <div class="enroll-time">
                  <div class="enroll-number"><h3>{{total || 1}}</h3>
                  </div>
                  <div class="enroll-text">今日登录
                  </div>
                </div>
            </el-col>
          </div>
          <div style="flex: 1;min-width: 180px;max-width:180px;height: 80px; display: flex;">
            <el-col :span="4" class="lightgreen-box">
              <div class="underline">
              <i class="el-icon-date"></i>
            </div>
            </el-col>
            <el-col :span="20" class="orange-box">
              <div class="enroll-time">
                  <div class="enroll-number"><h3>{{total || 7}}</h3>
                  </div>
                  <div class="enroll-text">三日新增
                  </div>
                </div>
            </el-col>
          </div>
          <div style="flex: 1;min-width: 180px;max-width:180px;height: 80px;display: flex;">
            <el-col :span="4" class="lightgreen-box">
              <div class="underline">
              <i class="el-icon-folder-add"></i>
            </div>
            </el-col>
            <el-col :span="20" class="orange-box">
              <div class="enroll-time">
                  <div class="enroll-number"><h3>{{total || 15}}</h3>
                  </div>
                  <div class="enroll-text">七日新增
                  </div>
                </div>
            </el-col>
          </div>
          <div style="flex: 1;min-width: 180px;max-width:180px;height: 80px; display: flex;">
            <el-col :span="4" class="lightgreen-box">
              <div class="underline">
              <i class="el-icon-user-solid"></i>
            </div>
            </el-col>
            <el-col :span="20" class="orange-box">
              <div class="enroll-time">
                  <div class="enroll-number"><h3>{{total || 24}}</h3>
                  </div>
                  <div class="enroll-text">七日活跃
                  </div>
                </div>
            </el-col>
          </div>
          <div style="flex: 1;min-width: 180px;max-width:180px;height: 80px; display: flex;">
            <el-col :span="4" class="lightgreen-box">
              <div class="underline">
              <i class="el-icon-user"></i>
            </div>
            </el-col>
            <el-col :span="20" class="orange-box">
              <div class="enroll-time">
                  <div class="enroll-number"><h3>{{total || 89}}</h3>
                  </div>
                  <div class="enroll-text">月活跃
                  </div>
                </div>
            </el-col>
          </div>  
        </div>
  </el-card>
  </template>
  
  <script>
  export default {
    title: '用户新增活跃图',
    icon: 'el-icon-user-solid',
    description: '用户新增',
    height: 28,
    minH: 8,
    width: 10,
    minW: 5,
    isResizable: true,
    data () {
      return {
        total: 0
      }
    },
    mounted () {
        this.initGet()
    },
    methods: {
        initGet () {
      request({
        url: ''
      }).then(res => {
        const { data } = res
        // this.total = data.total
      })
    },
    // 生成一个随机整数
    randomColor () {
      const color = [
        '#fffff',
      ]
      const ran = Math.floor(Math.random() * 4)
      return color[ran]
    }
  }
}
  </script>
  
  <style scoped>
  .card-view{
  border-radius: 10px;
  color: rgb(37,176,138);
}
.lightgreen-box {
   border-bottom: 2px solid  rgb(37,176,138);
      height:60px;
      margin-bottom: 10px;
    }
    .underline i{
        font-size: 30px;
      }
    .orange-box {
      height:60px;
      color: black;
      border-bottom:2px solid rgb(242,242,242);
    }
    .enroll-time{
      margin-left: 10px;
     }
    .enroll-text{
      color: rgb(138,138,138);
    }
  </style>
  