
<template>
  <el-drawer
    :visible.sync="drawer"
    direction="rtl"
    >
    <div>
      <el-timeline>
        <el-timeline-item
          v-for="(activity, index) in activities"
          :key="index"
          :icon="activity.icon"
          :type="activity.type"
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
      options:{},
      drawer: false,
      activities: [],
      timer: null
    }
  },
  methods: {
    getInit () {
      console.log(this.options.id)
      if (this.options.id) {
        const params = {
          id: this.options.id,
          _fields: 'import_log,'
        }
        api.getObj(params).then((res) => {
          const { data } = res.data
          const activities = JSON.parse(data.import_log)
          this.activities = activities.reverse()
        })
      }
    }
  },
  mounted () {
    const that = this
    //that.timer = setInterval(that.getInit, 3000)
  },
  created () {
    //this.getInit()
  },
  beforeDestroy () {
    clearInterval(this.timer)
  }
}
</script>
