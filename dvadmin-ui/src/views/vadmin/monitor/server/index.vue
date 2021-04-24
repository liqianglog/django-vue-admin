<template>
  <div class="app-container">
    <!-- 监控控制 -->
    <div class="server-monitor-control">
      <!-- 监控启用开关 -->
      <div class="control-server-monitor same-block">
        开启监控：
        <el-switch
          v-model="isOpeningMonitor"
          active-color="#13ce66"
          inactive-color="#ff4949"
          @change="changeMonitorStatus"
        >
        </el-switch>
      </div>
      <!-- 更新频率设置 -->
      <div class="monitor-update-interval same-block">
        更新频率：
        <el-input-number v-model="monitorUpdateInterval"
                         label=""
                         class="monitor-update-interval-blank"
                         controls-position="right"
                         :min="minMonitorUpdateInterval"
                         @input="handleIntervalChange"

        ></el-input-number>
        <el-select v-model="intervalType"
                   class="monitor-update-interval-unit"
                   @change="selectIntervalType"
        >
          <el-option
            v-for="item in Object.keys(INTERVAL_ID_TO_TYPE_MAPPING)"
            :key="INTERVAL_ID_TO_TYPE_MAPPING[item].type"
            :label="INTERVAL_ID_TO_TYPE_MAPPING[item].name"
            :value="INTERVAL_ID_TO_TYPE_MAPPING[item].name">
          </el-option>
        </el-select>

      </div>
      <!-- 监控日志保存时间 -->
      <div class="monitor-log-save-time same-block">
        保存天数：
        <el-input v-model="monitorLogSavingDays" class=" same-block" style="width: 120px;"></el-input>
        <el-button type="primary"
                   class="same-block"
                   @click="updateMonitorStatusSettingsInfo"
        >更改
        </el-button>
      </div>
      <!-- 清空记录 -->
      <div class="clean-monitor-log same-block">
        <el-button class="same-block" @click="cleanMonitorLogsInfo" type="warning">清空记录</el-button>
      </div>
    </div>
    <div class="server-monitor-top">
      <!-- 左侧服务器信息 -->
      <el-card class="box-card server-information">
        <div slot="header" class="clearfix">
          <div class="server-info-item">服务器</div>
          <el-select filterable
                     v-model="currentServerName"
                     class="server-info-item"
                     placeholder="请选择服务器"
                     @change="chooseServerInfo"
          >
            <el-option
              v-for="(item,index) in allServerInfo"
              :key="item.id"
              :label="item.name"
              :value="index"
            >
            </el-option>
          </el-select>
          <el-button type="primary" class="server-info-item" @click="updateServerInfo">更改</el-button>
        </div>
        <div class="server-info-detail">
          <div v-for="(key,index) in currentServerInfoKeys" :key="index" class="server-info-detail-line text item">
            <div class="server-info-detail-item">
              <div style="width: 30%;display: inline-block;">{{ SERVER_KEY_TO_NAME_MAPPING[key] }}:</div>
              <div v-if="CHANGEABLE_SERVER_FIELDS.indexOf(key) > -1" style="display: inline-block;">
                <el-input style="display: inline-block; width: 90%;" v-model="currentServer[key]"></el-input>
              </div>
              <div v-else style="display: inline-block; "> {{ currentServer[key] }}</div>
            </div>
          </div>
        </div>
      </el-card>

      <!-- 右侧仪表盘 -->
      <el-card class="box-card information-instrument-panel" v-for="(key, index)  of Object.keys(instrumentBoardData)"
               :key="`${index}-${key}`">
        <instrument-board
          :top-title="{show:true, text: key}"
          :ring-graph-id="`${key}UsingRate`"
          :using-rate="instrumentBoardData[key].rate"
          :top-title-key-to-name-mapping="INSTRUMENT_BOARD_KEY_TO_NAME_MAPPING"
          :sub-title="{show:true, used: instrumentBoardData[key].used, total:instrumentBoardData[key].total, unit: instrumentBoardData[key].unit}"
          :using-rate-style="{...getCircleColor(instrumentBoardData[key].rate)}"
        ></instrument-board>
      </el-card>
    </div>
    <!--  下方折线图  -->
    <div class="server-monitor-bottom">
      <!-- 折线图 -->
      <el-card class="box-card server-monitor-line-chart" v-for="(key, index) in Object.keys(lineChartData)"
               :key="`${index}-${key}`">
        <line-chart :line-chart-key="key"
                    :server-info="currentServer"
                    :chart-title="CHART_KEY_NAME_MAPPING[key]"
                    :chart-data="lineChartData[key]"
        ></line-chart>
      </el-card>
    </div>
  </div>
</template>

<script>
import {
  cleanMonitorLog,
  getMonitorLogs,
  getMonitorStatusInfo,
  getServerLatestLog,
  getServerList,
  updateMonitorStatusInfo,
  updateServerInfo
} from '@/api/vadmin/monitor/server'
import InstrumentBoard from '@/views/vadmin/monitor/server/components/InstrumentBoard'
import LineChart from '@/views/vadmin/monitor/server/components/LineChart'
import moment from 'moment'

const debounce = require('lodash/debounce')

// 要展示的信息，key -> name
const SERVER_KEY_TO_NAME_MAPPING = {
  ip: '服务器IP',
  name: '服务器名称',
  os: '操作系统',
  remark: '备注'
}

// 更新频率类型映射
const INTERVAL_ID_TO_TYPE_MAPPING = {
  0: {
    type: 0,
    name: '秒',
    key: 'seconds',
    second: 1
  },
  1: {
    type: 1,
    name: '分钟',
    key: 'minutes',
    second: 60
  },
  2: {
    type: 2,
    name: '小时',
    key: 'hours',
    second: 60 * 60
  },
  3: {
    type: 3,
    name: '天',
    key: 'days',
    second: 24 * 60 * 60
  }
}
const defaultUpdateInterval = INTERVAL_ID_TO_TYPE_MAPPING['0']

// 图表字段映射
const CHART_KEY_NAME_MAPPING = {
  cpu: 'CPU',
  memory: '内存',
  disk: '磁盘'
}

// 仪表盘字段映射
const INSTRUMENT_BOARD_KEY_TO_NAME_MAPPING = {
  cpu: "CPU使用率",
  memory: "内存使用率",
  disk: "磁盘使用率"
}

// 仪表盘颜色范围
const NORMAL_COLOR = {
  color: '#28BCFE',
  itemColor: ['#25bfff', '#5284de', '#2a95f9']
}
const WARNING_COLOR = {
  color: '#e6a23c',
  itemColor: ['#e6a23c', '#cc8b1d', '#ffaf18']
}
const DANGER_COLOR = {
  color: '#F56C6C',
  itemColor: ['#fd666d', '#cf1717', '#b31212']
}

// 服务器信息可修改字段
const CHANGEABLE_SERVER_FIELDS = ['name', 'remark']

export default {
  name: 'Server',
  components: {
    InstrumentBoard,
    LineChart
  },
  data() {
    return {
      SERVER_KEY_TO_NAME_MAPPING,
      INTERVAL_ID_TO_TYPE_MAPPING,
      CHART_KEY_NAME_MAPPING,
      CHANGEABLE_SERVER_FIELDS,
      INSTRUMENT_BOARD_KEY_TO_NAME_MAPPING,
      timeRange: [
        `${moment().format('YYYY-MM-DD')} 00:00:00`,
        `${moment().format('YYYY-MM-DD')} 23:59:59`
      ],
      // 加载层信息
      loading: [],
      // 所有服务器信息
      allServerInfo: [],
      // 当前展示的服务器名称
      currentServerName: '',
      // 当前展示的服务器信息
      currentServer: {},
      // 当前展示的服务器信息索引，更新服务器信息时用
      currentServerIndex: 0,
      // 开启监控控制按钮
      isOpeningMonitor: false,
      // 数据更新频率
      monitorUpdateInterval: 60,
      // 最小更新频率值
      minMonitorUpdateInterval: 0,
      // 更新频率类型
      intervalType: defaultUpdateInterval.name,
      // 更新频率单位对应秒
      intervalTypeUnits: defaultUpdateInterval.second,
      // 监控日志保存天数
      monitorLogSavingDays: 30,
      // 折线图数据
      lineChartData: {},
      // 仪表盘数据
      instrumentBoardData: {}
    }
  },
  computed: {
    currentServerInfoKeys() {
      return Object.keys(this.currentServer).filter(key => {
        if (SERVER_KEY_TO_NAME_MAPPING[key]) {
          return { [key]: SERVER_KEY_TO_NAME_MAPPING[key] }
        }
      })
    },
    intervalNameToSecondMapping() {
      let intervalNameToSecondMapping = {}
      Object.values(INTERVAL_ID_TO_TYPE_MAPPING).forEach(item => {
        intervalNameToSecondMapping[item.name] = item.second
      })
      return intervalNameToSecondMapping
    },
    monitorStatusInfo() {
      return {
        enabled: this.isOpeningMonitor ? 1 : 0,
        save_days: this.monitorLogSavingDays,
        interval: this.monitorUpdateInterval * this.intervalTypeUnits
      }
    }
  },
  watch: {
    currentServer(newServerInfo) {
      if (newServerInfo) {
        // 更新最新监控信息
        this.getServerLatestLogInfo(newServerInfo.id)
        // 获取监控日志信息
        this.getCurrentServerMonitorLogs()
      }
    }
  },
  created() {
    this.openLoading()
    // 获取所有服务器信息
    this.getServerList(this.currentServerIndex)
    // 获取服务器监控频率设置
    this.getMonitorStatusSettingsInfo()
  },
  methods: {
    /** 查询所有服务器基础信息 */
    getServerList(serverIndex) {
      getServerList({ pageNum: 'all' }).then(response => {
        this.allServerInfo = response.data
        if (this.allServerInfo.length > 0) {
          this.currentServer = this.allServerInfo[serverIndex || this.currentServerIndex]
          this.currentServerName = this.currentServer.name
        }
        this.loading.close()
      })
    },
    /**修改服务器信息*/
    updateServerInfo() {
      updateServerInfo(this.currentServer.id, this.currentServer).then(results => {
        this.msgSuccess(results.msg || '修改服务器信息成功！')
      }).catch(error => {
        this.$message.error(error.msg || '提交修改服务器信息出错！')
      })
    },
    /** 获取服务器最新监控信息 */
    getServerLatestLogInfo(serverId) {
      getServerLatestLog(serverId).then(results => {
        // this.instrumentBoardData = results.data
        this.instrumentBoardData = {
          cpu: {
            total: 2,
            used: '', // cpu核心 可不传，如指cpu当前主频，该值可以传
            rate: 12,
            unit: '核心' // 默认单位 核心
          },
          memory: {
            total: 1024,
            used: 512,
            rate: 70,
            unit: 'MB' // 默认单位 MB
          },
          disk: {
            total: 50,
            used: 30,
            rate: 90,
            unit: 'GB'  // 默认单位 GB
          }
        }
      }).catch(error => {
        this.msgError(error.msg || '获取服务器最新监控信息错误！')
      })
    },
    /** 获取监控日志信息 */
    getCurrentServerMonitorLogs() {
      getMonitorLogs(this.currentServer.id, { as: { 'create_datetime__range': this.timeRange } }).then(results => {
        // this.lineChartData = results.data
        this.lineChartData = {
          cpu: [0.5, 0.43, 0.56, 0.89, 0.5, 0.43, 0.56, 0.89, 0.5, 0.43, 0.56, 0.89, 0.5, 0.43, 0.56, 0.89],
          memory: [0.6, 0.43, 0.56, 0.56, 0.89, 0.5, 0.43, 0.43, 0.56, 0.56, 0.5, 0.43, 0.56, 0.89, 0.5]
        }
      }).catch(error => {
        this.msgError(error.msg || '获取监控日志信息出错误！')
      })
    },

    /** 清除监控日志 */
    cleanMonitorLogsInfo() {
      cleanMonitorLog().then(results => {
        this.msgSuccess(results.msg || '清除记录成功！')
      }).catch(error => {
        this.$message.warning(error.msg || '清除记录失败，请重试！')
      })
    },

    /** 获取监控配置信息 */
    getMonitorStatusSettingsInfo() {
      getMonitorStatusInfo().then(results => {
        let { enabled, interval, save_days } = results
        this.isOpeningMonitor = enabled
        this.monitorLogSavingDays = parseInt(save_days || 30)
        this.formatInterval(parseInt(interval))
      }).catch(error => {
        this.msgError(error.msg || '获取服务器监控配置信息出错误！')
      })
    },
    /** 更新监控配置信息 */
    updateMonitorStatusSettingsInfo() {
      updateMonitorStatusInfo(this.monitorStatusInfo).then(result => {
        this.msgSuccess(result.msg || '更新配置成功！')
      }).catch((error) => {
        this.msgError(error.msg || '更新服务器监控配置信息出错误！')
      })
    },

    // 打开加载层
    openLoading() {
      this.loading = this.$loading({
        lock: true,
        text: '拼命读取中',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      })
    },
    // 选择展示的服务器信息
    chooseServerInfo(index) {
      this.currentServerIndex = index
      this.currentServer = this.allServerInfo[index]
      this.currentServerName = this.currentServer.name
    },
    // 更改更新频率（周期）数值
    handleIntervalChange: debounce(function(value) {
      this.monitorUpdateInterval = value
    }, 500),
    // 选择更新频率（周期） 单位
    selectIntervalType(value) {
      this.intervalType = value
      this.intervalTypeUnits = this.intervalNameToSecondMapping[value]
    },
    // 修改监控状态
    changeMonitorStatus(value) {
      this.isOpeningMonitor = value
    },
    // 监控周期时间转换
    formatInterval(intervalTime) {
      let biggerInterval = 0
      for (let interval of Object.values(INTERVAL_ID_TO_TYPE_MAPPING)) {
        if (interval.second > biggerInterval && interval.second < intervalTime) {
          biggerInterval = interval.second
          this.monitorUpdateInterval = intervalTime / interval.second
          this.intervalType = interval.name
          this.intervalTypeUnits = interval.second
        }
      }
    },
    // 仪表盘样式-颜色
    getCircleColor(usingRate) {
      if (usingRate < 60) {
        return NORMAL_COLOR
      } else if (usingRate > 60 && usingRate < 80) {
        return WARNING_COLOR
      } else if (usingRate > 80) {
        return DANGER_COLOR
      }
    }
  }
}
</script>
<style scoped>
.el-button--medium {
  margin: 2px;
  padding: 10px 10px;
}

.server-monitor-top {
  padding: 0 10px;
  text-align: justify-all;
}

.server-monitor-bottom {
  text-align: left;
}

.server-information {
  width: 20%;
  min-width: 400px;
  min-height: 300px;
  display: inline-block;
}

.information-instrument-panel {
  display: inline-block;
  min-height: 300px;
  min-width: 400px;
  margin: 0 10px;
}

.server-info-item {
  display: inline-block;
  margin: 0 5px;
}

.server-info-detail {
  min-height: 200px;
}

.server-info-detail-line {
  margin: 5px;
  min-height: 20px;
}

.server-info-detail-item {
  text-align: justify;
  line-height: 40px;
  margin: 4px 0;
  overflow: auto;
}

.server-monitor-control {
  width: 100%;
  height: 60px;
  line-height: 60px;
  padding: 0 20px;
}

.monitor-update-interval {
  margin: 0 20px;
}

.same-block {
  display: inline-block;
}

.monitor-update-interval-blank {
  width: 100px;
  margin: 0 2px;
}

.monitor-update-interval-unit {
  width: 80px;
  margin: 0 2px;
}

.monitor-log-save-time {
  width: 280px;
  margin: 0 2px;
}

.clean-monitor-log {
}


.server-monitor-line-chart {
  height: 400px;
  width: 45%;
  min-width: 500px;
  margin: 10px;
  display: inline-block;
}

</style>
