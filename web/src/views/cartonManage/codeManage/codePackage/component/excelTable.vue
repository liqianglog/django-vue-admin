<!--
 * @创建文件时间: 2021-12-14 16:16:23
 * @Auther: 猿小天
 * @最后修改人: 猿小天
 * @最后修改时间: 2021-12-17 16:03:01
 * 联系Qq:1638245306
 * @文件介绍:
-->
<template>
  <el-container>
    <el-main>
      <!-- <el-descriptions :column="2" border>
        <template slot="extra">
          <el-button type="primary" size="small">导出</el-button>
        </template>
        <el-descriptions-item label="订单编号">
          {{ objData.id }}
        </el-descriptions-item>
        <el-descriptions-item label="订单名称">
          {{ objData.name }}
        </el-descriptions-item>
        <el-descriptions-item label="包内文件数量(个)">
          {{ objData.code_package_count }}
        </el-descriptions-item>
        <el-descriptions-item label="订单数量(万)"> 0 </el-descriptions-item>
        <el-descriptions-item label="每包数量(万)"> 0 </el-descriptions-item>
        <el-descriptions-item label="导入成功数量(万)">
          0
        </el-descriptions-item>
        <el-descriptions-item label="包内重码数量(个)">
          0
        </el-descriptions-item>
        <el-descriptions-item label="历史对比重码(万)">
          0
        </el-descriptions-item>
        <el-descriptions-item label="下单人"> 无 </el-descriptions-item>
        <el-descriptions-item label="导入负责人">
          {{ objData.creator_name }}
        </el-descriptions-item>
        <el-descriptions-item label="导入时间">
          {{ objData.create_datetime }}
        </el-descriptions-item>
      </el-descriptions> -->

      <table
        width="100%"
        border="0"
        cellspacing="1"
        cellpadding="4"
        bgcolor="#cccccc"
        class="tabtop13"
        align="center"
      >
        <tr>
          <td class="btbg font-center titfont" colspan="2">导入报告</td>
        </tr>
        <tr>
          <td width="20%" class="btbg1 font-center">订单编号</td>
          <td>{{ objData.id }}</td>
        </tr>
        <tr>
          <td width="20%" class="btbg1 font-center">订单名称</td>
          <td>{{ objData.name }}</td>
        </tr>
        <tr>
          <td width="20%" class="btbg1 font-center">包内文件数量(个)</td>
          <td>{{ objData.code_package_count }}</td>
        </tr>
        <tr>
          <td width="20%" class="btbg1 font-center">订单总码数量(个)</td>
          <td>{{ objData.order_sum_number }} ({{objData.order_sum_number/10000}}万)</td>
        </tr>
        <tr>
          <td width="20%" class="btbg1 font-center">每包数量(个)</td>
          <td>{{ objData.single_code_package_number }} ({{objData.single_code_package_number/10000}}万)</td>
        </tr>
        <tr>
          <td width="20%" class="btbg1 font-center">导入成功数量(个)</td>
          <td>{{ objData.success_code_data_number }} ({{objData.success_code_data_number/10000}}万)</td>
        </tr>
        <tr>
          <td width="20%" class="btbg1 font-center">导入负责人</td>
          <td>{{ objData.creator_name }}</td>
        </tr>
        <tr>
          <td width="20%" class="btbg1 font-center">导入开始时间</td>
          <td>{{ objData.create_datetime }}</td>
        </tr>
        <tr>
          <td width="20%" class="btbg1 font-center">导入结束时间</td>
          <td>{{ objData.update_datetime }}</td>
        </tr>
      </table>
    </el-main>
  </el-container>
</template>

<script>
import * as api from '../api'
export default {
  props: {
    options: {
      type: Object,
      default () {
        return {}
      }
    }
  },
  data () {
    return {
      objData: {}
    }
  },
  methods: {
    getList () {
      if (this.options.mainId) {
        const params = {
          id: this.options.mainId
        }
        api.getExportReport(params).then((res) => {
          const { data } = res
          this.objData = data
        })
      }
    }
  },
  created () {
    this.getList()
  }
}
</script>

<style lang="scss" scope>
.tabtop13 {
  margin-top: 13px;
}
.tabtop13 td {
  background-color: #ffffff;
  height: 25px;
  line-height: 150%;
}
.font-center {
  text-align: center;
}
.btbg {
  background: #e9faff !important;
}
.btbg1 {
  background: #f2fbfe !important;
}
.btbg2 {
  background: #f3f3f3 !important;
}
.biaoti {
  font-family: 微软雅黑;
  font-size: 26px;
  font-weight: bold;
  border-bottom: 1px dashed #cccccc;
  color: #255e95;
}
.titfont {
  font-family: 微软雅黑;
  font-size: 16px;
  font-weight: bold;
  color: #255e95;
  background-color: #e9faff;
}
.tabtxt2 {
  font-family: 微软雅黑;
  font-size: 14px;
  font-weight: bold;
  text-align: right;
  padding-right: 10px;
  color: #327cd1;
}
.tabtxt3 {
  font-family: 微软雅黑;
  font-size: 14px;
  padding-left: 15px;
  color: #000;
  margin-top: 10px;
  margin-bottom: 10px;
  line-height: 20px;
}
</style>
