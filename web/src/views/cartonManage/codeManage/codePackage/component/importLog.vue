<template>
  <el-drawer
    :visible.sync="drawer"
    direction="rtl"
    size="800px"
  >
    <div slot="title">
      <span>码包订单导入报告</span>
      <el-tag size="small" style="margin-left: 10px">{{
          options.order_id
        }}
      </el-tag>
    </div>
    <dva-html2pdf :filename="String(options.no) + '码包订单导入报告'" :company="'供应商: '+ info.tenant_name">
      <div style="margin: 10px;z-index: -1">
        <h1 style="font-size: 24px;text-align: center;margin-bottom: 20px;color: #000;">码包订单导入报告</h1>
        <el-row :gutter="20" style="margin-bottom: 10px;">
          <el-col :span="18">
            <el-card class="box-card-state">
              <div style="text-align: center">
                <el-row :gutter="20">
                  <el-col :span="8">
                    <div class="title">码包总数</div>
                    <div class="content">{{ options.total_number }}</div>
                  </el-col>
                  <el-col :span="8">
                    <div class="title">本码包重码数</div>
                    <div class="content">{{ options.package_repetition_number }}</div>
                  </el-col>
                  <el-col :span="8">
                    <div class="title">历史码包重码数</div>
                    <div class="content">{{ options.database_repetition_number > 1000? '1000+' : options.database_repetition_number }}</div>
                  </el-col>
                </el-row>
                <br>
                <el-row :gutter="20">
                  <el-col :span="8">
                    <div class="title">来源</div>
                    <div class="content">{{ options.source_label }}</div>
                  </el-col>

                  <el-col :span="8">
                    <div class="title">导入耗时(秒)</div>
                    <div class="content">{{ objData.import_run_time }}</div>
                  </el-col>
                </el-row>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="box-card" style="padding: 0;">
              <div style="text-align: center">
              <span v-if="options.validate_status === 4">
                <i style="color:#65B687;font-size: 100px;margin-top: 10px;margin-bottom: 5px;"
                   class="el-icon-success"></i>
                <br>
                <span style="font-size: 14px;color:#65B687">校验通过</span>
              </span>
                <span v-if="options.validate_status === 3">
                <i style="color:red;font-size: 100px;margin-top: 10px;margin-bottom: 5px;" class="el-icon-error"></i>
                <br>
                <span style="font-size: 14px;color:red;">校验失败</span>
              </span>
              </div>
            </el-card>
          </el-col>
        </el-row>
        <el-row :gutter="20" style="margin-bottom: 10px;">
          <el-col :span="24">
            <el-card class="box-card-details">
              <div>
                <navTitle>基础信息</navTitle>
                <ul class="overview_info" style="padding: 10px;padding-bottom: 0;">
                  <li>
                    <span class="item_title">码包编号：</span>
                    <span>{{ objData.no }} </span>
                  </li>
                  <li>
                    <span class="item_title">码包名称：</span>
                    <span>{{ objData.zip_name }} </span>
                  </li>
                  <li>
                    <el-row :gutter="20" style="margin-bottom: 10px;">
                      <el-col :span="12">
                        <span class="item_title">订单编号：</span>
                        <span>{{ objData.order_id }} </span>
                      </el-col>
                      <el-col :span="12">
                        <span class="item_title">产品名称：</span>
                        <span>{{ objData.product_name }} </span>
                      </el-col>
                    </el-row>
                  </li>
                  <li>
                    <el-row :gutter="20" style="margin-bottom: 10px;">
                      <el-col :span="12">
                        <span class="item_title">码长度：</span>
                        <span>{{ objData.char_length }}</span>
                      </el-col>
                      <el-col :span="12">
                        <span class="item_title">字段数：</span>
                        <span>{{ objData.fields }}</span>
                      </el-col>
                    </el-row>
                  </li>
                  <li>
                    <el-row :gutter="20" style="margin-bottom: 10px;">
                      <el-col :span="12">
                        <span class="item_title">导入开始时间：</span>
                        <span>{{ formatDatetime(objData.import_start_datetime) }}</span>
                      </el-col>
                      <el-col :span="12">
                        <span class="item_title">导入完成时间：</span>
                        <span>{{ formatDatetime(objData.import_end_datetime) }}</span>
                      </el-col>
                    </el-row>
                  </li>
                </ul>
              </div>
            </el-card>
          </el-col>
        </el-row>
        <el-row :gutter="20" style="margin-bottom: 10px;">
          <el-col :span="24">
            <el-card class="box-card-details">
              <div>
                <navTitle>导入日志</navTitle>
                <table class="statistics_table">
                  <thead>
                  <tr>
                    <th width="160">校验内容</th>
                    <th width="100" style="text-align: center">校验结果</th>
                    <th width="180" style="text-align: center">校验时间</th>
                    <th width="200" style="text-align: center">其他说明</th>
                    <th width="20" style="text-align: center"></th>
                  </tr>
                  </thead>
                  <tbody>
                  <tr v-for="(item,index) in JSON.parse(objData.import_log)" :key="index"
                      :class="{error:item.type==='error'}"
                      :style="{'border-bottom': JSON.parse(objData.import_log).length === index+1 ?'none':''}">
                    <td width="160">{{ item.content }}</td>
                    <td width="100" style="text-align: center;">
                      <el-tag size="mini" :type="item.type==='error'?'danger':'success'">{{ item.result }}</el-tag>
                    </td>
                    <td width="180" style="text-align: center">{{ item.timestamp }}</td>
                    <td width="200" style="text-align: center">{{ item.remark }}</td>
                    <td width="20" style="text-align: center"></td>
                  </tr>
                  </tbody>
                </table>
              </div>
            </el-card>
          </el-col>
        </el-row>
        <div class="html2pdf__page-break" v-if="objData.repetition_data.length > 0"/>
        <el-row :gutter="20" v-if="objData.repetition_data.length > 0">
          <el-col :span="24">
            <el-card class="box-card-details">
              <div>
                <navTitle>重码记录</navTitle>
                <table class="statistics_table">
                  <thead>
                  <tr>
                    <th width="260">重码内容</th>
<!--                    <th width="100" style="text-align: center">码类型</th>-->
                    <th width="180" style="text-align: center">重码时间</th>
                    <th width="20" style="text-align: center"></th>
                  </tr>
                  </thead>
                  <tbody>
                  <tr v-for="(item,index) in objData.repetition_data" :key="index"
                      :style="{'border-bottom': objData.repetition_data.length === index+1 ?'none':''}">
                    <td width="260">{{ item.code_content }}</td>
                    <td width="180" style="text-align: center">{{ formatDatetime(item.create_datetime) }}</td>
                    <td width="20" style="text-align: center"></td>
                  </tr>
                  </tbody>
                </table>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </dva-html2pdf>
  </el-drawer>
</template>

<script>
import * as api from '../api'
import dayjs from 'dayjs'
import navTitle from './navTitle'
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState('d2admin/user', ['info'])
  },
  components: {
    navTitle
  },
  data () {
    return {
      options: {},
      drawer: false,
      objData: {
        zip_name: null,
        total_number: null,
        product_name: null,
        arrival_factory: null,
        import_start_datetime: null,
        import_end_datetime: null,
        import_run_time: null,
        import_log: null,
        repetition_data: [],
        char_length: null,
        fields: null,
        w_url_prefix: null,
        n_url_prefix: null
      },
      timer:null
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
    this.timer = setTimeout(() => {
      this.getInit()
    }, 3000)
  },
  beforeDestroy() {
    clearTimeout(this.timer)
  }
}
</script>

<style lang="scss" scope>
.overview_info {
  li {
    list-style: none;
    line-height: 30px;
    background-color: #f8fbff;
    margin-bottom: 10px;
    font-size: 14px;
    color: #333333;

    .item_title {
      width: 140px;
      padding-left: 10px;
      display: inline-block;
    }
  }
}

.statistics_table {
  //text-align: center;
  border-collapse: collapse;
  border-spacing: 0;
  margin-left: 10px;
  margin-bottom: 5px;
  margin-right: 20px;
  width: 750px;
  padding: 10px;
}

.statistics_table tbody tr {
  border-bottom: 1px solid #ebebeb;
  font-size: 14px;
  text-align: center;
}

.statistics_table thead {
  border-top: 1px solid #ebebeb;
  border-bottom: 1px solid #ebebeb;
  font-size: 14px;
}

.statistics_table td,
.statistics_table th {
  font-size: 14px;
  height: 35px;
  text-align: left;
}

.el-drawer__body {
  background-color: #FAFAFA;
}

.el-drawer__header {
  margin-bottom: 0px;
}

.box-card .el-card__body {
  padding: 5px;
}

.box-card-details .el-card__body {
  padding: 0;

  .report-title {
    border-top-right-radius: 35px;
    border-bottom-right-radius: 35px
  }
}

.box-card-state {
  text-align: center;

  .title {
    color: #A9A9A9;
    font-size: 14px
  }

  .content {
    color: #000;
    font-size: 16px;
    font-weight: 600;
  }
}

.error {
  color: red;
}

</style>
