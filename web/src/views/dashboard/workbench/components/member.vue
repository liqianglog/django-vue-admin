<template>
    <el-card class="card-view" :style= "{backgroundColor:randomColor()}" shadow="always">
      <div>
        <el-row type="flex" justify="space-around" style="padding:10px">
          <el-col :span="12">
            <div class="card-content">
              <div class="card-content-label">用户总数</div>
              <div class="card-content-value">{{sum_register}}</div>
            </div>
          </el-col>
          <el-col :span="6" :offset="6" style="text-align: right;">
            <i class="el-icon-user-solid" size="48px"></i>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </template>
  
  <script>
  import { request } from '@/api/service'
  
  export default {
    title: '用户总数',
    icon: 'el-icon-user-solid',
    description: '总会员数',
    name: 'summarizing',
    height: 14,
    width: 8,
    minH: 14,
    minW: 8,
    isResizable: true,
    data () {
      return {
        sum_register:"",
      }
    },
    methods: {
      initGet () {
      request({
        url: '/api/system/homepage_statistics/'
      }).then((res)=>{
     this.sum_register=res.data.sum_register
      })
    },
      // 生成一个随机整数
      randomColor () {
        const color = [
          '#50A8F4FF',
          '#FD6165FF',
          '#E679D8FF',
          '#F9AB5BFF'
        ]
        const ran = Math.floor(Math.random() * 4)
        return color[ran]
      }
    },
    mounted () {
      this.initGet()
    }
  }
  </script>
  
  <style scoped lang="scss">
  .card-view{
    border-radius: 10px;
    color: #FFFFFF;
    .card-content{ 
      .card-content-label{
        font-size: 1em;
        color: #FFFFFF;
      }
      .card-content-value{
        color: #FFFFFF;
        margin-top: 10px;
        font-size: 1.5em;
        font-weight: bold;
      }
    }
  }
  .el-icon-user-solid{
     font-size: 30px; 
  }
  </style>
  