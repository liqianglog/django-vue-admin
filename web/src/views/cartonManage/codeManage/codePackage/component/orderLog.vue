
<template>
  <el-drawer
    :visible.sync="drawer"
    direction="rtl"
    >
    <div slot="title">
      <span>码包导入日志</span>
      <el-tag size="small" style="margin-left: 10px">{{
          options.order_id
        }}</el-tag>
      <el-tag size="small" style="margin-left: 10px" :type="options.validate_status === 4 ?'success':'danger'">{{
          {1:'待校验',2:'校验中',3:'校验失败',4:'校验通过'}[options.validate_status]
        }}</el-tag>
    </div>
    <div style="margin-left: 2em;">
      <el-timeline>
        <el-timeline-item
          v-for="(activity, index) in activities"
          :key="index"
          :icon="activity.icon"
          :type="activity.type==='error'?'danger':activity.type"
          :color="activity.color"
          :size="activity.size"
          :timestamp="activity.timestamp"
        >
          {{ activity.content }}
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
            console.log(activities)
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
