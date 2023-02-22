<template>
  <el-card shadow="hover" header="设备信息">
    <div>
      <el-row>
        <el-col :span="8">
          <el-statistic :value="objData.device_total" title="设备总数"></el-statistic>
        </el-col>
        <el-col :span="8">
          <el-statistic :value="objData.verify_device" title="检测设备总数"></el-statistic>
        </el-col>
        <el-col :span="8">
          <el-statistic :value="objData.prod_device" title="生产设备总数"></el-statistic>
        </el-col>
      </el-row>
    </div>
    <div style="margin-top: 10px">
      <el-table
        :data="objData.list"
        height="260"
        border
        style="width: 100%">
        <el-table-column
          prop="no"
          label="设备编号"
          width="180">
        </el-table-column>
        <el-table-column
          prop="name"
          label="设备类型"
          width="180">
        </el-table-column>
        <el-table-column
          prop="production_status"
          label="生产状态">
          <template v-slot="{row}">
            <div v-for="(item,index) in status_list" :key="index">
              <el-tag size="mini" v-if="item.value===row.type"  :type="item.type">{{ item.label }}</el-tag>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </el-card>
</template>

<script>
import '@/plugin/dragx'
import {request} from "@/api/service";

export default {
  title: '设备信息',
  icon: 'el-icon-setting',
  description: '设备信息的展示',
  height: 40,
  width: 8,
  minH: 80,
  minW: 8,
  isResizable: true,
  data() {
    return {
      status_list:[
        {value:0, label:"码包管理端",type: 'success'},
        {value:1, label:"检测管理端",type:'danger'}
      ],
      objData: {
        device_total: 0,
        verify_device: 0,
        prod_device: 0,
        list: []
      }
    }
  },
  methods:{
    initGet(){
      request({
        url:'/api/datav/index/device_info/'
      }).then(res=>{
        const {data} = res
        this.objData = data
      })
    }
  },
  mounted() {
    this.initGet()
  }
}
</script>

<style scoped>
.item-background p {
  color: #999;
}
</style>
