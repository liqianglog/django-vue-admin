<template>
<!--  <el-container>-->
<!--    <el-main>-->
<!--      <table-->
<!--        width="100%"-->
<!--        border="0"-->
<!--        cellspacing="1"-->
<!--        cellpadding="4"-->
<!--        bgcolor="#cccccc"-->
<!--        class="tabtop13"-->
<!--        align="center"-->
<!--      >-->
<!--        <tr>-->
<!--          <td class="btbg font-center titfont" colspan="2">导入报告</td>-->
<!--        </tr>-->
<!--        <tr>-->
<!--          <td width="20%" class="btbg1 font-center">订单编号</td>-->
<!--          <td>{{ objData.id }}</td>-->
<!--        </tr>-->
<!--        <tr>-->
<!--          <td width="20%" class="btbg1 font-center">订单名称</td>-->
<!--          <td>{{ objData.name }}</td>-->
<!--        </tr>-->
<!--        <tr>-->
<!--          <td width="20%" class="btbg1 font-center">包内文件数量(个)</td>-->
<!--          <td>{{ objData.code_package_count }}</td>-->
<!--        </tr>-->
<!--        <tr>-->
<!--          <td width="20%" class="btbg1 font-center">订单总码数量(个)</td>-->
<!--          <td>{{ objData.order_sum_number }} ({{objData.order_sum_number/10000}}万)</td>-->
<!--        </tr>-->
<!--        <tr>-->
<!--          <td width="20%" class="btbg1 font-center">每包数量(个)</td>-->
<!--          <td>{{ objData.single_code_package_number }} ({{objData.single_code_package_number/10000}}万)</td>-->
<!--        </tr>-->
<!--        <tr>-->
<!--          <td width="20%" class="btbg1 font-center">导入成功数量(个)</td>-->
<!--          <td>{{ objData.success_code_data_number }} ({{objData.success_code_data_number/10000}}万)</td>-->
<!--        </tr>-->
<!--        <tr>-->
<!--          <td width="20%" class="btbg1 font-center">导入负责人</td>-->
<!--          <td>{{ objData.creator_name }}</td>-->
<!--        </tr>-->
<!--        <tr>-->
<!--          <td width="20%" class="btbg1 font-center">导入开始时间</td>-->
<!--          <td>{{ objData.create_datetime }}</td>-->
<!--        </tr>-->
<!--        <tr>-->
<!--          <td width="20%" class="btbg1 font-center">导入结束时间</td>-->
<!--          <td>{{ objData.update_datetime }}</td>-->
<!--        </tr>-->
<!--      </table>-->
<!--    </el-main>-->
<!--  </el-container>-->
  <el-drawer
    :visible.sync="drawer"
    direction="rtl"
    size="800px"
  >
    <div slot="title">
      <span>码包导入报告</span>
      <el-tag size="small" style="margin-left: 10px">{{
          options.order_id
        }}</el-tag>
    </div>
    <div style="padding: 0em 1em">
      <el-descriptions column="1">
        <el-descriptions-item label="压缩包名称">{{objData.zip_name}}</el-descriptions-item>
        <el-descriptions-item label="码包总数">
          <el-tag size="small">{{objData.total_number}}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="码类型">
          <el-tag size="small">{{objData.code_type}}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="产品名称">{{objData.product_name}}</el-descriptions-item>
        <el-descriptions-item label="到货工厂">{{objData.arrival_factory}}</el-descriptions-item>
        <el-descriptions-item label="导入开始时间">{{formatDatetime(objData.import_start_datetime)}}</el-descriptions-item>
        <el-descriptions-item label="导入结束时间">{{formatDatetime(objData.import_end_datetime)}}</el-descriptions-item>
        <el-descriptions-item label="导入耗时时长">{{objData.import_run_time}}</el-descriptions-item>
        <el-descriptions-item label="码总长度">{{objData.char_length}}</el-descriptions-item>
        <el-descriptions-item label="码字段数">{{objData.fields}}</el-descriptions-item>
      </el-descriptions>
    </div>
  </el-drawer>
</template>

<script>
import * as api from '../api'
import dayjs from 'dayjs'
export default {
  data () {
    return {
      options: {},
      drawer: false,
      objData: {
        zip_name: null,
        total_number: null,
        code_type: null,
        product_name: null,
        arrival_factory: null,
        import_start_datetime: null,
        import_end_datetime: null,
        import_run_time: null,
        import_log: null,
        char_length: null,
        fields: null,
        w_url_prefix: null,
        n_url_prefix: null
      }
    }
  },
  methods: {
    formatDatetime (val) {
      return dayjs(val).format('YYYY-MM-DD HH:mm:ss')
    },
    getInit () {
      const that = this
      if (this.options.id) {
        const params = {
          id: that.options.id
        }
        api.getImportReport(params).then((res) => {
          const { data } = res
          // console.log(data)
          that.objData = data
        })
      }
    }
  },
  created () {

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
