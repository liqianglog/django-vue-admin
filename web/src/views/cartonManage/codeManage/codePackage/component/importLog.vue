<template>
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
      <navTitle>基础信息</navTitle>
      <ul class="overview_info">
        <li>
          <span class="item_title">码包编号：</span>
          <span>{{ objData.no }} </span>
        </li>
        <li>
          <span class="item_title">订单编号：</span>
          <span>{{ objData.order_id }} </span>
        </li>
        <li>
          <span class="item_title">码包名称：</span>
          <span>{{ objData.zip_name }} </span>
        </li>
        <li>
          <span class="item_title">码包总数：</span>
          <span>{{ objData.total_number }} </span>
        </li>
        <li>
          <span class="item_title">码类型：</span>
          <span>{{ objData.code_type }} </span>
        </li>
        <li>
          <span class="item_title">外码网址：</span>
          <span>{{objData.w_url_prefix}}</span>
        </li>
        <li>
          <span class="item_title">内码网址：</span>
          <span>{{objData.n_url_prefix}}</span>
        </li>
        <li>
          <span class="item_title">产品名称：</span>
          <span>{{ objData.product_name }} </span>
        </li>
        <li>
          <span class="item_title">到货工厂：</span>
          <span>{{ objData.arrival_factory }}</span>
        </li>

        <li>
          <span class="item_title">码长度：</span>
          <span>{{objData.char_length}}</span>
        </li>
        <li>
          <span class="item_title">字段数：</span>
          <span>{{objData.fields}}</span>
        </li>
        <li>
          <span class="item_title">导入开始时间：</span>
          <span>{{ objData.import_start_datetime }}</span>
        </li>
        <li>
          <span class="item_title">导入完成时间：</span>
          <span>{{ objData.import_end_datetime }}</span>
        </li>
        <li>
          <span class="item_title">导入耗时时长：</span>
          <span>{{objData.import_run_time}}</span>
        </li>
      </ul>
      <navTitle>导入日志</navTitle>
      <table class="statistics_table">
        <thead>
        <tr>
          <th width="200">校验内容</th>
          <th width="200">校验结果</th>
          <th width="200">校验时间</th>
          <th width="200">其他说明</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(item,index) in JSON.parse(objData.import_log)" :key="index">
          <td width="200">{{item.content}}</td>
          <td width="200" style="text-align: center">{{item.result}}</td>
          <td width="200" style="text-align: center">{{item.timestamp}}</td>
          <td width="200" style="text-align: center">{{item.remark}}</td>
        </tr>
        </tbody>
      </table>
      <br>
    </div>
  </el-drawer>
</template>

<script>
import * as api from '../api'
import dayjs from 'dayjs'
import navTitle from './navTitle'
export default {
  components:{
    navTitle
  },
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
.overview_info {
  li {
    list-style: none;
    line-height: 40px;
    background-color: #f8fbff;
    margin-bottom: 10px;
    color: #333;
    .item_title {
      width: 200px;
      display: inline-block;
    }
  }
}

::v-deep .statistics_table {
  //text-align: center;
  border-collapse: collapse;
  border-spacing: 0;
  margin-left: 10px;
  margin-bottom: 5px;
  margin-right: 10px;
  width: 100%;
}
::v-deep .statistics_table tbody tr {
  border-bottom: 1px solid #ebebeb;
  font-size: 0.8em;
  text-align: center;
}
::v-deep .statistics_table thead {
  border-top: 1px solid #ebebeb;
  border-bottom: 1px solid #ebebeb;
  font-size: 1em;
}
::v-deep .statistics_table td,
::v-deep .statistics_table th {
  height: 40px;
  text-align: left;
}
</style>
