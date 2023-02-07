
<template>
  <el-drawer
    :visible.sync="drawer"
    direction="rtl"
    >
    <div slot="title">
      <span>码包订单导入日志</span>
      <el-tag size="small" style="margin-left: 10px">{{
          options.order_id
        }}</el-tag>
      <el-tag size="small" style="margin-left: 10px" :type="options.validate_status === 4 ?'success':'danger'">{{
          {1:'待校验',2:'校验中',3:'校验失败',4:'校验通过'}[options.validate_status]
        }}</el-tag>
    </div>
    <div class="time-line">

    <el-timeline :reverse="true">
      <el-timeline-item
        v-for="(activity, index) in activities"
        :key="index"
        size="large"
        :icon="activity.icon || (activity.type==='error'?'el-icon-close':'el-icon-check')"
        :type="activity.type==='error'?'danger':activity.type"
      >
        <div class="time">
          <div class="day">{{ activity.timestamp }}</div>
        </div>
        <div class="ml10">
          <div class="list-title">{{ activity.content }}</div>
          <div class="error list-company" v-if="activity.type==='error'">{{ activity.result }}</div>
          <div class="list-company" v-else>{{ activity.result }}</div>
          <div class="list-desc" v-if="activity.remark && activity.remark !== '-'">{{ activity.remark }}</div>
        </div>
      </el-timeline-item>
    </el-timeline>
    </div>
  </el-drawer>
</template>
<script>
import * as api from './../api'
import { mapState } from 'vuex'
export default {
  computed: {
    ...mapState('productionVuex', {
      brandOwnerOrderId: (state) => state.brandOwnerOrderId
    })
  },
  data () {
    return {
      options: {},
      drawer: false,
      activities: [],
      timer: null
    }
  },
  methods: {
    getInit () {
      const that = this
      if (this.options.id) {
        const params = {
          id: this.options.id
        }
        api.viewLog(params).then((res) => {
          const { data } = res
          if (data) {
            const activities = JSON.parse(data)
            if (this.options.validate_status === 2) {
              activities.push({
                icon: 'el-icon-loading',
                type: 'primary',
                content: '正在校验中...',
                result: '请等待'
              })
            }
            if (this.options.validate_status === 1) {
              activities.push({
                icon: 'el-icon-more',
                type: 'primary',
                content: '正在排队等待校验中...',
                result: '请等待'
              })
            }
            that.activities = activities
          }
        })
      }
    }
  },
  mounted () {
    // that.timer = setInterval(that.getInit, 3000)
  },
  created () {
    // this.getInit()
  },
  beforeDestroy () {
    clearInterval(this.timer)
  }
}
</script>

<style lang="scss" scoped>
  .time-line {
    margin-left: 200px;
  }
  .error{
    color: red!important;
  }
  .list-title {
    font-size: 16px;
    font-family: PingFangSC-Medium, PingFang SC;
    font-weight: 500;
    color: #181b1e;
  }
  .list-company {
    font-size: 14px;
    font-family: PingFangSC-Regular, PingFang SC;
    font-weight: 400;
    color: #2991ff;
    margin-top: 15px;
    margin-bottom: 15px;
  }
  .list-desc {
    font-size: 14px;
    font-family: PingFangSC-Regular, PingFang SC;
    font-weight: 400;
    color: #596878;
  }
  //左侧时间
  .time {
    color: #409eff;
    position: absolute;
    left: -154px;
    top: 1px;
    .day {
      font-size: 14px;
      font-family: PingFangSC-Regular, PingFang SC;
      font-weight: 400;
      color: #596878;
      text-align: center;
    }
  }
</style>
