<template>
  <el-card shadow="hover" header="设备信息">
    <div>
      <el-row>
        <el-col :span="8">
          <el-statistic :value="objData.verify_total" title="设备总数"></el-statistic>
        </el-col>
        <el-col :span="8">
          <el-statistic :value="objData.verify_error_type_0" title="未识别数"></el-statistic>
        </el-col>
        <el-col :span="8">
          <el-statistic :value="objData.verify_error_type_2" title="码不存在数"></el-statistic>
        </el-col>
        <el-col :span="8">
          <el-statistic :value="objData.verify_error_type_3" title="本检测码包"></el-statistic>
        </el-col>
        <el-col :span="8">
          <el-statistic :value="objData.verify_error_type_4" title="本生产工单重码数"></el-statistic>
        </el-col>
        <el-col :span="8">
          <el-statistic :value="objData.verify_error_type_5" title="非本生产工单码数"></el-statistic>
        </el-col>
      </el-row>
    </div>
  </el-card>
</template>

<script>
import '@/plugin/dragx'
import { request } from '@/api/service'

export default {
  title: '检测问题码信息',
  icon: 'el-icon-setting',
  description: '检测问题码的信息展示',
  height: 20,
  width: 8,
  minH: 20,
  minW: 8,
  isResizable: true,
  data () {
    return {
      objData: {
        verify_total: 0,
        verify_error_type_0: 0,
        verify_error_type_2: 0,
        verify_error_type_3: 0,
        verify_error_type_4: 0,
        verify_error_type_5: 0
      }
    }
  },
  methods: {
    initGet () {
      request({
        url: '/api/datav/index/verify_code_record/'
      }).then(res => {
        const { data } = res
        this.objData = data
      })
    }
  },
  mounted () {
    this.initGet()
  }
}
</script>

<style scoped>
.item-background p {
  color: #999;
}
</style>
